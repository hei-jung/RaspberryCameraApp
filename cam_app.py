"""
1. 카메라 어플
- 기능::
어플 실행하자마자 사진 미리보기(촬영모드 버튼 누르면 다시 사진 미리보기로)
버튼(촬영모드: 촬영모드, 흑백, 컬러 / 저장된 사진: 이전, 다음, 삭제)
"""
import os
import time
import cv2 as cv
import threading
import tkinter as tk


class CamApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # UI 초기화
        self.master = master
        self.master.geometry("400x400+200+400")
        self.master.resizable(True, True)
        self.pack()
        self.create_widgets()  # 위젯 초기화
        self.mode = 1  # 라디오버튼 모드
        self.cap = None  # 카메라 캡처
        self.color = cv.COLOR_BGR2BGRA  # 기본 촬영 모드: 컬러 ---> -가 되도록 self.color 초기화
        self.images = []  # img 폴더 안에 저장된 파일 목록
        self.img_pos = 0  # img 폴더 안에 저장된 파일을 가리키는 인덱스

    def create_widgets(self):
        """위젯 초기화"""
        self.mode = tk.IntVar()  # 라디오버튼 모드 가져오기

        # 촬영모드 라디오버튼
        self.rbtn_s = tk.Radiobutton(self, text="촬영모드", variable=self.mode.get(), value=1)
        self.rbtn_s["command"] = self.shoot
        self.rbtn_s.pack()
        self.rbtn_s.select()  # 처음엔 '촬영모드'에 체크돼있는 상태. '촬영모드'를 실행하지는 않음

        # 사진모드 라디오버튼
        self.rbtn_v = tk.Radiobutton(self, text="사진모드", variable=self.mode.get(), value=2)
        self.rbtn_v["command"] = self.view
        self.rbtn_v.pack()

        # 사진 촬영하는 버튼: 찰칵!
        self.btn_s = tk.Button(self)
        self.btn_s["text"] = "찰칵!"
        self.btn_s["command"] = self.save_img
        self.btn_s.pack(fill='x')
        self.btn_s["state"] = "disabled"

        # 촬영 흑백 모드 버튼
        self.btn_gray = tk.Button(self)
        self.btn_gray["text"] = "흑백"
        self.btn_gray["command"] = self.set_gray
        self.btn_gray.pack(fill='x')
        self.btn_gray["state"] = "disabled"

        # 촬영 컬러 모드 버튼
        self.btn_color = tk.Button(self)
        self.btn_color["text"] = "컬러"
        self.btn_color["command"] = self.set_color
        self.btn_color.pack(fill='x')
        self.btn_color["state"] = "disabled"

        # 이전 사진 보기 버튼
        self.btn_prev = tk.Button(self)
        self.btn_prev["text"] = "이전"
        self.btn_prev["command"] = self.previous_img
        self.btn_prev.pack(side='left')
        self.btn_prev["state"] = "disabled"

        # 다음 사진 보기 버튼
        self.btn_next = tk.Button(self)
        self.btn_next["text"] = "다음"
        self.btn_next["command"] = self.next_img
        self.btn_next.pack(side='left')
        self.btn_next["state"] = "disabled"

        # 현재 사진 삭제 버튼
        self.btn_del = tk.Button(self)
        self.btn_del["text"] = "삭제"
        self.btn_del["command"] = self.del_img
        self.btn_del.pack(side='left')
        self.btn_del["state"] = "disabled"

        self.img = tk.PhotoImage(file="")
        self.img_viewer = tk.Label(self.master, image=self.img)
        self.img_viewer.pack()

    def preview(self):
        """촬영 미리보기"""
        print("촬영 미리보기")
        self.cap = cv.VideoCapture(0)
        'width: {0}, height: {1}'.format(self.cap.get(3), self.cap.get(4))
        self.cap.set(3, 320)
        self.cap.set(4, 240)
        while 1:
            ret, frame = self.cap.read()
            if ret:
                cap_color = cv.cvtColor(frame, self.color)
                cv.imshow('shoot preview', cap_color)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv.destroyAllWindows()

    def shoot(self):
        """촬영모드"""
        print("촬영모드")
        # 촬영 미리보기 쓰레드로 실행
        t_photo = threading.Thread(target=self.preview, args=())
        t_photo.start()
        # 촬영모드 --> 촬영과 관련된 버튼: 활성화, 사진 보기와 관련된 버튼: 비활성화
        self.btn_s["state"] = "normal"
        self.btn_gray["state"] = "normal"
        self.btn_color["state"] = "normal"
        self.btn_prev["state"] = "disabled"
        self.btn_next["state"] = "disabled"
        self.btn_del["state"] = "disabled"

    def save_img(self):
        """사진 저장: 파일명은 (현재 날짜 및 시간).png 형태 EX. 20200618155248.png"""
        photo_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        file_name = 'img/' + photo_time + '.png'
        print(file_name, '저장')

        ret, img = self.cap.read()
        img = cv.cvtColor(img, self.color)  # 현재 지정된 촬영모드(흑백, 컬러)로 저장
        cv.imshow('photo saved', img)
        cv.imwrite(file_name, img)

    def view(self):
        """사진모드"""
        print("사진모드")
        # 사진모드 --> 촬영과 관련된 버튼: 비활성화, 사진 보기와 관련된 버튼: 활성화
        self.btn_s["state"] = "disabled"
        self.btn_gray["state"] = "disabled"
        self.btn_color["state"] = "disabled"
        self.btn_next["state"] = "normal"
        self.btn_del["state"] = "normal"
        self.images = os.listdir('img/')
        # 마지막으로 가리키고 있던 위치의 사진을 보여준다.
        self.img = tk.PhotoImage(file='img/' + self.images[self.img_pos], format='png')
        self.img_viewer["image"] = self.img

    def set_gray(self):
        """촬영 - 흑백 모드"""
        print("흑백모드")
        self.color = cv.COLOR_BGR2GRAY

    def set_color(self):
        """촬영 - 컬러모드"""
        print("컬러모드")
        self.color = cv.COLOR_BGR2BGRA

    def previous_img(self):
        """이전 사진 보여주기"""
        print("이전")
        self.images = os.listdir('img/')
        self.img_pos -= 1
        self.img = tk.PhotoImage(file='img/' + self.images[self.img_pos], format='png')
        self.img_viewer["image"] = self.img
        if self.img_pos == len(self.images) - 2:
            # '이전' 버튼을 누르기 직전에 마지막 사진이었을 때,
            # '이전' 버튼을 누르고 나면 '다음' 버튼 활성화
            self.btn_next["state"] = "normal"
        elif self.img_pos == 0:
            # '이전' 버튼을 누르고 난 사진이 첫번째 사진이면, 버튼 비활성화
            self.btn_prev["state"] = "disabled"

    def next_img(self):
        """다음 사진 보여주기"""
        print("다음")
        self.images = os.listdir('img/')
        self.img_pos += 1
        self.img = tk.PhotoImage(file='img/' + self.images[self.img_pos], format='png')
        self.img_viewer["image"] = self.img
        if self.img_pos == 1:
            # '다음' 버튼을 누르기 직전에 첫번째 사진이었을 때,
            # '다음' 버튼을 누르고 나면 '이전' 버튼 활성화
            self.btn_prev["state"] = "normal"
        elif self.img_pos == len(self.images) - 1:
            # '다음' 버튼을 누르고 난 사진이 마지막 사진이면, 버튼 비활성화
            self.btn_next["state"] = "disabled"

    def del_img(self):
        """현재 레이블에 보이는 사진 삭제"""
        print('img/' + self.images[self.img_pos] + " 삭제")
        os.remove('img/' + self.images[self.img_pos])
        self.images = os.listdir('img/')  # 파일명 리스트 새로고침
        # 이미지 레이블의 사진을 이전 사진으로 새로고침
        self.img_pos -= 1
        self.img = tk.PhotoImage(file='img/' + self.images[self.img_pos], format='png')
        self.img_viewer["image"] = self.img
        if self.img_pos == 0:
            self.btn_prev["state"] = "disabled"
        elif self.img_pos == len(self.images) - 1:
            self.btn_next["state"] = "disabled"


class Main:
    def __init__(self):
        root = tk.Tk()
        self.cam_app = CamApp(master=root)

    def run(self):
        self.cam_app.mainloop()


if __name__ == '__main__':
    main = Main()
    main.run()
