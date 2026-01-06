import sys
try:
    import sklearn
    print(f"Sklearn version: {sklearn.__version__}")
    from sklearn.utils import check_random_state
    print("Sklearn utils ok")
except Exception as e:
    print(f"Sklearn Error: {e}")

try:
    import imblearn
    print(f"Imblearn version: {imblearn.__version__}")
    from imblearn.over_sampling import RandomOverSampler
    print("Imblearn ok")
except Exception as e:
    print(f"Imblearn Error: {e}")
