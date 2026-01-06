from fastapi import APIRouter, HTTPException
import os
import requests
from dotenv import load_dotenv
from models import ContactRequest

load_dotenv()

router = APIRouter(tags=["Contact"])

@router.post("/contact")
async def send_contact_email(request: ContactRequest):
    """
    Send a contact email via Unosend.
    """
    # 1. Verify Turnstile Token
    cloudflare_secret = os.getenv("CLOUDFLARE_SECRET_KEY")
    if cloudflare_secret and request.turnstile_token:
        verify_url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
        verify_payload = {
            "secret": cloudflare_secret,
            "response": request.turnstile_token
        }
        try:
            verify_res = requests.post(verify_url, json=verify_payload)
            verify_data = verify_res.json()
            if not verify_data.get("success"):
                raise HTTPException(status_code=400, detail="CAPTCHA verification failed")
        except requests.exceptions.RequestException:
             # If verification service is down, maybe fail open or closed depending on security needs
             # For now, let's log and proceed or fail? Failsafe closed is better for spam.
             print("Failed to contact Cloudflare verification service")
             raise HTTPException(status_code=500, detail="CAPTCHA verification service error")
    elif cloudflare_secret and not request.turnstile_token:
         raise HTTPException(status_code=400, detail="CAPTCHA token missing")

    unosend_api_key = os.getenv("UNOSEND_API_KEY")
    if not unosend_api_key:
        print("UNOSEND_API_KEY is not set") # Log error
        raise HTTPException(status_code=500, detail="Server configuration error")

    url = "https://www.unosend.co/api/v1/emails"
    headers = {
        "Authorization": f"Bearer {unosend_api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "from": "contact@techterview.dev", 
        "to": ["francismistica06@gmail.com"], 
        "reply_to": request.email,
        "subject": f"New Contact Form Submission: {request.subject}",
        "html": f"""
            <h2>New Message from {request.name}</h2>
            <p><strong>Email:</strong> {request.email}</p>
            <p><strong>Subject:</strong> {request.subject}</p>
            <br>
            <p><strong>Message:</strong></p>
            <p>{request.message}</p>
        """
    }

    # 1. Send Admin Notification
    try:
        response = requests.post(url, json=payload, headers=headers)
        if not response.ok:
             print(f"Unosend API Error (Admin): {response.status_code} - {response.text}")
        response.raise_for_status()
        admin_email_id = response.json().get("id")
    except requests.exceptions.RequestException as e:
        error_detail = "Failed to send email"
        if e.response is not None:
             print(f"Response: {e.response.text}")
             error_detail = f"Unosend API Error: {e.response.text}"
        print(f"Unosend API error: {str(e)}")
        raise HTTPException(status_code=500, detail=error_detail)

    # 2. Send User Confirmation (Auto-Response)
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Contact Confirmation</title>
    </head>
    <body style="margin: 0; padding: 0; background-color: #f4f4f5; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
      <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f5; padding: 40px 0;">
        <tr>
          <td align="center">
            <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);">
              
              <!-- Header -->
              <tr>
                <td style="padding: 40px 40px 30px 40px; background-color: #ffffff; border-bottom: 1px solid #e4e4e7;">
                   <h1 style="margin: 0; color: #18181b; font-size: 24px; font-weight: 700; letter-spacing: -0.5px;">DheKode</h1>
                   <p style="margin: 5px 0 0 0; color: #71717a; font-size: 14px;">Powered by A.S.P.I.R.E.</p>
                </td>
              </tr>

              <!-- Content -->
              <tr>
                <td style="padding: 40px;">
                  <h2 style="margin: 0 0 20px 0; color: #18181b; font-size: 20px; font-weight: 600;">Hello, {request.name}!</h2>
                  <p style="margin: 0 0 24px 0; color: #52525b; font-size: 16px; line-height: 1.6;">
                    Thank you for reaching out to us. We have received your inquiry regarding the <strong>A.S.P.I.R.E. System</strong>.
                  </p>
                  <p style="margin: 0 0 30px 0; color: #52525b; font-size: 16px; line-height: 1.6;">
                    Our team is currently reviewing your message and will get back to you shortly.
                  </p>
                  
                  <div style="background-color: #f4f4f5; border-radius: 8px; padding: 20px; border: 1px solid #e4e4e7;">
                    <p style="margin: 0 0 10px 0; color: #71717a; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600;">Your Message</p>
                    <p style="margin: 0; color: #3f3f46; font-size: 15px; line-height: 1.5; font-style: italic;">
                      "{request.message}"
                    </p>
                  </div>
                </td>
              </tr>

              <!-- Footer -->
              <tr>
                <td style="padding: 30px 40px; background-color: #fafafa; border-top: 1px solid #e4e4e7;">
                  <p style="margin: 0 0 10px 0; color: #71717a; font-size: 14px; line-height: 1.5;">
                    © 2025 LSPU CCS Thesis Project. All rights reserved.
                    <br>
                    <span style="font-size: 12px; color: #a1a1aa;">Automated Skill Prediction & Industry Reasoning Engine</span>
                  </p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """

    user_payload = {
        "from": "contact@techterview.dev",
        "to": [request.email],
        "subject": f"Confirmation: {request.subject}",
        "html": html_content
    }
    
    try:
        # We don't want to fail the whole request if the auto-response fails, but we should log it.
        user_response = requests.post(url, json=user_payload, headers=headers)
        if not user_response.ok:
            print(f"Unosend Auto-Response Error: {user_response.status_code} - {user_response.text}")
    except Exception as e:
        print(f"Failed to send auto-response: {str(e)}")

    return {"status": "success", "message": "Email sent successfully", "id": admin_email_id}
