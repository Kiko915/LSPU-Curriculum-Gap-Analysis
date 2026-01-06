import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { motion, type HTMLMotionProps } from "framer-motion"
import { Controller, FormProvider, useFormContext } from "react-hook-form"
import type { ControllerProps, FieldPath, FieldValues } from "react-hook-form"

import { cn } from "@/lib/utils"
import { Label } from "@/components/ui/label"

const Form = FormProvider

type FormFieldContextValue<
    TFieldValues extends FieldValues = FieldValues,
    TName extends FieldPath<TFieldValues> = FieldPath<TFieldValues>
> = {
    name: TName
}

const FormFieldContext = React.createContext<FormFieldContextValue>(
    {} as FormFieldContextValue
)

type FormItemContextValue = {
    id: string
}

const FormItemContext = React.createContext<FormItemContextValue>(
    {} as FormItemContextValue
)

const FormField = <
    TFieldValues extends FieldValues = FieldValues,
    TName extends FieldPath<TFieldValues> = FieldPath<TFieldValues>
>({
    ...props
}: ControllerProps<TFieldValues, TName>) => {
    return (
        <FormFieldContext.Provider value={{ name: props.name }}>
            <Controller {...props} />
        </FormFieldContext.Provider>
    )
}

const useFormField = () => {
    const fieldContext = React.useContext(FormFieldContext)
    const itemContext = React.useContext(FormItemContext)
    const { getFieldState, formState } = useFormContext()


    const fieldState = getFieldState(fieldContext.name, formState)

    if (!fieldContext) {
        throw new Error("useFormField should be used within <FormField>")
    }

    const { id } = itemContext

    return {
        id,
        name: fieldContext.name,
        formItemId: `${id}-form-item`,
        formDescriptionId: `${id}-form-item-description`,
        formMessageId: `${id}-form-item-message`,
        ...fieldState,
    }
}

const FormItem = React.forwardRef<
    HTMLDivElement,
    React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => {
    const id = React.useId()

    return (
        <FormItemContext.Provider value={{ id }}>
            <div ref={ref} className={cn("space-y-2", className)} {...props} />
        </FormItemContext.Provider>
    )
})
FormItem.displayName = "FormItem"

const FormLabel = React.forwardRef<
    React.ElementRef<typeof Label>,
    React.ComponentPropsWithoutRef<typeof Label>
>(({ className, ...props }, ref) => {
    const { error, formItemId } = useFormField()

    return (
        <Label
            ref={ref}
            className={cn(error && "text-destructive", className)}
            htmlFor={formItemId}
            {...props}
        />
    )
})
FormLabel.displayName = "FormLabel"

const FormControl = React.forwardRef<
    React.ElementRef<typeof Slot>,
    React.ComponentPropsWithoutRef<typeof Slot>
>(({ ...props }, ref) => {
    const { error, formItemId, formDescriptionId, formMessageId } = useFormField()

    return (
        <Slot
            ref={ref}
            id={formItemId}
            aria-describedby={
                !error
                    ? `${formDescriptionId}`
                    : `${formDescriptionId} ${formMessageId}`
            }
            aria-invalid={!!error}
            {...props}
        />
    )
})
FormControl.displayName = "FormControl"

const FormDescription = React.forwardRef<
    HTMLParagraphElement,
    React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => {
    const { formDescriptionId } = useFormField()

    return (
        <p
            ref={ref}
            id={formDescriptionId}
            className={cn("text-[0.8rem] text-muted-foreground", className)}
            {...props}
        />
    )
})
FormDescription.displayName = "FormDescription"

const FormMessage = React.forwardRef<
    HTMLParagraphElement,
    HTMLMotionProps<"p">
>(({ className, children, ...props }, ref) => {
    const { error, formMessageId } = useFormField()
    const body = (error ? String(error?.message) : children) as React.ReactNode

    if (!body) {
        return null
    }

    return (
        <motion.p
            ref={ref}
            id={formMessageId}
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className={cn("text-[0.8rem] font-medium text-destructive flex items-center gap-2 mt-2", className)}
            {...props}
        >
            <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="currentColor"
                className="size-4 shrink-0"
            >
                <path
                    fillRule="evenodd"
                    d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12ZM12 8.25a.75.75 0 0 1 .75.75v3.75a.75.75 0 0 1-1.5 0V9a.75.75 0 0 1 .75-.75Zm0 8.25a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Z"
                    clipRule="evenodd"
                />
            </svg>
            {body}
        </motion.p>
    )
})
FormMessage.displayName = "FormMessage"

export {
    useFormField,
    Form,
    FormItem,
    FormLabel,
    FormControl,
    FormDescription,
    FormMessage,
    FormField,
}
