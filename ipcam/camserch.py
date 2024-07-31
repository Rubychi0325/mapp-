from onvif import ONVIFCamera

def get_rtsp_url(ip, port, user, password):
    # 創建ONVIF攝像機實例
    cam = ONVIFCamera(ip, port, user, password)
    
    # 獲取媒體服務
    media_service = cam.create_media_service()
    
    # 獲取媒體配置
    profiles = media_service.GetProfiles()
    media_profile = profiles[0]  # 選擇第一個配置檔案
    
    # 獲取RTSP流地址
    stream_setup = {
        'Stream': 'RTP-Unicast',
        'Transport': {'Protocol': 'RTSP'}
    }
    uri = media_service.GetStreamUri(StreamSetup=stream_setup, ProfileToken=media_profile.token)
    
    return uri.Uri

# 使用示例
ip = "192.168.2.67"  # 攝像機IP
port = 80            # ONVIF端口，通常為80或者8080
user = "admin"       # 使用者名稱
password = "admin"   # 密碼

rtsp_url = get_rtsp_url(ip, port, user, password)
print(f"RTSP URL: {rtsp_url}")