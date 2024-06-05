from PIL import Image,ImageDraw,ImageFont
from pathlib import Path


schedule = 0






class Schedule():
    def __init__(self):
        path = Path(__file__).parent
        self.img = Image.open(f'{path}\media\schedule_clear.jpg')

        self.i1 = ImageDraw.Draw(self.img)

        self.font = ImageFont.truetype(f'{path}\media\FFGoodProXCond-Regular.ttf',25)
        y = 100
        coordinates_monday = [7,y]
        coordinates_tuesday = [225,y]
        coordinates_wednesday = [442,y]
        coordinates_thursday = [660,y]
        coordinates_friday = [877,y]
        self.coordinates = [coordinates_monday,coordinates_tuesday,coordinates_wednesday,coordinates_thursday,coordinates_friday]
        spacing = 35

    def draw_subject(self,index_day:int,subjects:list):
       

        coordinates_ = self.coordinates[index_day]
        y= 100
        for i in range(len(subjects)):
            if subjects[i]!= None:
                self.i1.text((coordinates_[0],y),f'{i+1}.{subjects[i]}',font=self.font,fill=(0,0,0))
                y+= 35

    def save_pic(self):
        self.img.save('siga.png')

if __name__ == '__main__':
    a = Schedule()
    for i in range(0,5):
        a.draw_subject(i,['asdadsa'])

    a.save_pic()