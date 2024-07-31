import cv2
import numpy as np
from pyzbar.pyzbar import decode

# カメラを初期化
cap = cv2.VideoCapture(0)
#出力ウィンドウの設定
cap.set(3,640)
cap.set(3,480)

# QRコードを読み取る
while True:
    # フレームを取得
    ret, frame = cap.read()
    
    # QRコードをデコード
    decoded_objects = decode(frame)
    
    # QRコードが検出された場合
    if decoded_objects:
        for obj in decoded_objects:
            # QRコードの内容を表示
            print("検出されたQRコード:", obj.data.decode('utf-8'))
            
            # QRコードの位置を矩形で表示
            points = obj.polygon
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                cv2.polylines(frame, [hull], True, (0, 255, 0), 2)
            else:
                cv2.polylines(frame, [np.array(points, dtype=np.int32)], True, (0, 255, 0), 2)
        
        # 結果を表示
        cv2.imshow("QR Code Reader", frame)
        cv2.waitKey(2000)  # 2秒間結果を表示
        break
    
    # 'q'キーが押されたら終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# カメラを解放し、ウィンドウを閉じる
cap.release()
cv2.destroyAllWindows()