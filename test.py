import cv2
import time
from datetime import datetime
import pandas as pd


# カメラデバイス取得
# DirectshowはMicrosoftが提供しているビデオ（マルチメディア）を扱う際の様々なコンポーネントの集合体です。
# プログラムの要求に応じてビデオの加工、再生、録画、フォーマット変換などの処理を行うことができます。
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Directshowの設定
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 180)  # 幅180px
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 180) # 高さ180px
detector = cv2.QRCodeDetector() # QRCodeの読み取り機能を取得


if not cap.isOpened():
    print("カメラが開けません")
    exit()
else:
    print("カメラを開きました")


last_data = None
last_detected_time = 0
debounce_time = 3  # 秒単位
start_time = time.time()  # プログラムの開始時刻を記録


# 最終出力結果を出すためのリスト
# # データフレームにします。
list_summary = []


while True:
    # カメラから1フレーム読み取り
    ret, frame = cap.read()
    if not ret:
        print("フレームを読み取れません")
        break


    # QRコードを認識（グレースケールに変換して試す）
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    data, bbox, rectified_image = detector.detectAndDecode(gray_frame)


    # デバッグ用の詳細な出力
    current_time = time.time()
    if bbox is not None and len(bbox) > 0:
        print(f"QRコード検出: {bbox}")


        if data:
            list_data = []
            last_data = data
            last_detected_time = current_time
            print(f"QRコードデータ: {data}")  # ここでQRコードのテキスト情報を表示
            print(f"検出日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            list_data.append(data)
            list_data.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            list_summary.append(list_data)
            
            # バウンディングボックスの描画
            bbox = bbox.astype(int)
            for i in range(len(bbox)):
                cv2.polylines(frame, [bbox], True, (0, 255, 0), 2)
        else:
            print("QRコードデータがありません")  # デバッグ用にデータがない場合の出力
            time.sleep(0.1)
    else:
        print("QRコードが検出されませんでした")
        time.sleep(0.1)


    # ウィンドウ表示
    cv2.imshow('frame', frame)


    # 文字コードの検出と終了処理
    key = cv2.waitKey(1)
    if key == ord('q') or key == ord('Q'):
        break


    # 現在の時間が開始時間から20秒を超えているかチェック
    if current_time - start_time > 20:
        print("20秒が経過したため終了します")
        break


    # 処理負荷を軽減するための軽微な遅延
    time.sleep(0.1)


# 終了処理
cap.release()
cv2.destroyAllWindows()


col_name = ['name_hash', 'scan_time']
print(list_summary)
df = pd.DataFrame(list_summary) # リストをデータフレームにする
df.columns = col_name # 列名を追加
df.to_csv(r'C:\temp\libe_qrReader_code\result_0708\result_2.csv')


print('end')