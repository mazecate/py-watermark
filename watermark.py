import os
from PIL import Image, ImageDraw, ImageFont

def add_watermark_to_file(file_path, output_folder, watermark_text):
    """
    為單一圖片檔案加上文字水印
    """
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')
    if not file_path.lower().endswith(valid_extensions):
        print(f"跳過非圖片檔案: {file_path}")
        return

    filename = os.path.basename(file_path)
    output_path = os.path.join(output_folder, filename)

    try:
        # 開啟圖片並轉為 RGBA 模式（支援透明度）
        with Image.open(file_path) as img:
            img = img.convert("RGBA")
            
            # 建立一個與圖片大小相同的透明圖層用來畫水印
            txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(txt_layer)
            
            # 設定字體大小
            font_size = 40
            
            try:
                # Windows 系統常見字型
                font = ImageFont.truetype("arial.ttf", font_size)
            except IOError:
                try:
                    # Mac 系統常見字型
                    font = ImageFont.truetype("/Library/Fonts/Arial.ttf", font_size)
                except IOError:
                    # 預設字型
                    font = ImageFont.load_default()
                
            # 計算水印位置（右下角）
            image_width, image_height = img.size
            bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = image_width - text_width - 30
            y = image_height - text_height - 30
            
            # 繪製紅色水印 (RGB: 255, 0, 0, 透明度: 200)
            draw.text((x, y), watermark_text, fill=(255, 0, 0, 200), font=font)
            
            # 合併圖層並轉回 RGB
            watermarked = Image.alpha_composite(img, txt_layer).convert("RGB")
            
            # 儲存圖片
            watermarked.save(output_path)
            print(f"成功為圖片加上水印：{filename}")
            
    except Exception as e:
        print(f"處理圖片 {filename} 時發生錯誤: {e}")

def process_watermark(input_path, output_folder, watermark_text):
    """
    自動判斷 input_path 是單一檔案還是資料夾並進行處理
    """
    # 確保輸出資料夾存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 判斷輸入是資料夾還是單一檔案
    if os.path.isdir(input_path):
        print(f"偵測到資料夾，開始批次處理：{input_path}")
        for filename in os.listdir(input_path):
            file_full_path = os.path.join(input_path, filename)
            if os.path.isfile(file_full_path):
                add_watermark_to_file(file_full_path, output_folder, watermark_text)
    elif os.path.isfile(input_path):
        print(f"偵測到單一檔案，開始處理：{input_path}")
        add_watermark_to_file(input_path, output_folder, watermark_text)
    else:
        print(f"錯誤：找不到指定的檔案或資料夾「{input_path}」")

if __name__ == "__main__":
    # ==================== 設定區 ====================
    # INPUT_PATH 可以填寫：
    # 1. 單一圖片檔案名稱，例如："my_photo.jpg"
    # 2. 資料夾名稱，例如："input_images"
    INPUT_PATH = "f"     # <--- 修改這裡：可以填單檔或資料夾
    OUTPUT_DIR = "f_out"    # 儲存結果的資料夾
    WATERMARK_TEXT = "@name"    # 水印文字
    # ================================================
    
    process_watermark(INPUT_PATH, OUTPUT_DIR, WATERMARK_TEXT)
