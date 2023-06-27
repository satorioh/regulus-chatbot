import ast
import os


def main():
    is_prod = ast.literal_eval(os.getenv('IS_PROD'))
    print("应用启动中...")
    if is_prod:
        print("prod环境：")
        os.system("doppler run -- uvicorn main:app --host 0.0.0.0 --port 80")
    else:
        print("dev环境：")
        os.system("doppler run -- uvicorn main:app --reload")


main()
