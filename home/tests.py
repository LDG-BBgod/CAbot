from PIL import Image, ImageChops
import io
import requests


class Sunbae_Automation:
    def __init__(self, imgURL_path, imgLocal_path):
        self.__imgURL_path = imgURL_path
        self.__imgLocal_path = imgLocal_path

    def __getImage(self,path):
        response = requests.get(path)
        image_bytes = io.BytesIO(response.content)
        imgURL = Image.open(image_bytes)
        return imgURL

    def isAttendance(self):
        isFlag = True

        img1 = self.__getImage(self.__imgURL_path)
        img2 = Image.open(self.__imgLocal_path)

        try:            
            diff = ImageChops.difference(img1.convert('RGB'), img2.convert('RGB'))
            # 다른 부분이 있는지?
            if diff.convert('RGB').getbbox():
                isFlag = False
                # 다른 부분에 대한 값이 있는 경우 불일치
            else:
                isFlag = True
                print(diff.convert('RGB').getbbox())
        except:
            isFlag = True

        return isFlag