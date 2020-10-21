from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import cv2

# Create your views here.

def removeView(request):
    return render(request, 'index.html')

def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES.get('videoname',False)
        if not uploaded_file:
            context['url'] = '/media/slomo.MOV'
            context['modurl'] = context['url'] + '.mp4'
            return render(request, 'index.html', context)

        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
        tujuan = context['url'][1:]
        modfile = tujuan + '.mp4'
        context['modurl'] = context['url']+'.mp4'
        cap = cv2.VideoCapture(tujuan)
        # 재생할 파일의 넓이와 높이
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print("재생할 파일 넓이, 높이 : %d, %d" % (width, height))
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        #fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        #fourcc = 0x31637661
        out = cv2.VideoWriter(modfile, fourcc, 30.0, (int(height), int(width)))

        ret, pos_frame = cap.read()
        while (cap.isOpened()):
            ret, frame = cap.read()

            if ret == False:
                break;
            result = cv2.addWeighted(pos_frame, 0.5, frame, 0.5, 0)
            result = cv2.transpose(result)
            result = cv2.flip(result, 1)
            out.write(result)
            pos_frame = frame

        cap.release()
        out.release()

    return render(request,'index.html', context)
