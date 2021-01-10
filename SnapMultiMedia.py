from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import urllib.request
from pafy import *
import humanize
import os.path
import re
from subprocess import *
from moviepy.editor import *
from pafy.util import xenc

ui, _ = uic.loadUiType("SnapMultiMedia.ui")
"""
SnapMultiMedia :
Desktop Application to Download
Files , video from YouTube and 
Social Media, Convert Video to Audio
and Merge Audio and Video
"""
"""
Reference:
https://zulko.github.io/moviepy/index.html
https://docs.python.org/3/library/subprocess.html
https://you-get.org/
https://doc.qt.io/qt-5/reference-overview.html
https://pythonhosted.org/Pafy/
https://docs.python.org/3.8/library/urllib.request.html#module-urllib.request
https://docs.python.org/3/library/re.html
https://pypi.org/project/PyQt5/
https://docs.python.org/3/library/os.html
https://pypi.org/project/humanize/
"""


class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Button()
        self.InitUI()

    def InitUI(self):

        self.tabWidget.tabBar().setVisible(False)
        # to hide tab in widget
        self.Move_Box_1()
        self.Move_Box_2()
        self.Move_Box_3()
        self.Move_Box_4()
        # to make animation

    def Handel_Button(self):
        self.DownlodFile_Button.clicked.connect(self.Download)
        self.SaveFileButton.clicked.connect(self.File_Browser)
        self.GetDataButton.clicked.connect(self.Get_Video_data)
        self.SaveVideoButton.clicked.connect(self.Save_Browser)
        self.DownloadVideoButton.clicked.connect(self.Download_video)
        self.DownloadPlaylistButton.clicked.connect(self.Playlist_Downloads)
        self.SavePlaylistButton.clicked.connect(self.PlayList_Save)
        self.DownlodSocialVideoButton.clicked.connect(self.Download_Social_Video)
        self.SaveVideoSocialButton.clicked.connect(self.Save_Social_Video)

        self.Video_BrowseButton.clicked.connect(self.Convert_Video_Browse)
        self.Audio_SaveButton.clicked.connect(self.Convert_Audio_Browse)
        self.convertButton.clicked.connect(self.Convert_from_Video_to_Audio)

        self.HomeButton.clicked.connect(self.Open_Home)
        self.FileButton.clicked.connect(self.Open_Download)
        self.YoutubButton.clicked.connect(self.Open_YouTub)
        self.SocialButton.clicked.connect(self.Open_Social)
        self.ConvertButton.clicked.connect(self.Open_Convert)

        self.MergeButton.clicked.connect(self.Merge_Video_and_Audio)
        self.VideoMerge_BrowseButton.clicked.connect(self.Merge_Video_Browse)
        self.Audio_Merge_BrowseButton.clicked.connect(self.Merge_Audio_Browse)
        self.Merge_SaveButton.clicked.connect(self.Merge_Browse)

    ##################
    # File Downloads #
    ##################

    def Download(self):
        download_url = self.File_url.text()
        # get url of file
        save_location = self.Save_file.text()
        # to get path to save file
        if download_url == "" or save_location == "":
            QMessageBox.warning(self, " Data Error", "Provide URL or Save location")
        else:
            try:
                urllib.request.urlretrieve(download_url, save_location, self.File_Progress)
                # to download file using urllib.request module
                # urlretrieve to Copy a network object denoted by a URL to a local file
                QMessageBox.information(self, "Download Complete", "The Download Complete Successfully")
            except Exception:
                QMessageBox.warning(self, "Data Error", "Please, Provide a valid URL or Save locations")
        self.Save_file.setText("")
        self.File_url.setText("")
        self.progressBar.setValue(0)

    def File_Progress(self, block_num, block_size, total_size):
        read_data = block_num * block_size
        if total_size > 0:
            download_percentage = read_data * 100 / total_size
            self.progressBar.setValue(download_percentage)
            QApplication.processEvents()

    def File_Browser(self):
        save_location = QFileDialog.getSaveFileName(self, caption="Save As",
                                                    directory=".", filter="All Files(*.*)")

        self.Save_file.setText(str(save_location[0]))

    ###########################
    # YouTube Video Downloads #
    ###########################
    def Get_Video_data(self):
        video_url = self.Video_URL.text()
        if video_url == "":
            QMessageBox.warning(self, " Data Error", "Provide URL or Save location")
        else:
            video = pafy.new(video_url)
            # create an pafy object
            video_stream = video.streams
            # A list of regular streams (both audio and video)
            for stream in video_stream:
                size = humanize.naturalsize(stream.get_filesize())
                # get size of video and using "natural size" to make it readable for human
                data = "{} {} {} {} ".format(stream.mediatype, stream.extension,
                                             stream.quality, size)

                self.comboBox.addItem(data)

    def generate_filename(self, title, extension):
        max_length = 400
        ok = re.compile(r'[^/]')

        if os.name == "nt":
            ok = re.compile(r'[^\\/:*?"<>|]')

        filename = "".join(x if ok.match(x) else "_" for x in title)

        if max_length:
            max_length = max_length + 1 + len(extension)
            if len(filename) > max_length:
                filename = filename[:max_length - 3] + '...'

        filename += "." + extension
        return xenc(filename)

    def get_file_name_for_saving(self, save_location, full_name):
        file_path_with_name = os.path.join(save_location, full_name)
        if os.path.exists(file_path_with_name):
            split = file_path_with_name.split(".")
            file_path_with_name = ".".join(split[:-1]) + "1." + split[-1]

        return file_path_with_name

    def Download_video(self):
        video_url = self.Video_URL.text()
        # get url of video
        save_location = self.Save_Video.text()
        # get path to save video
        if video_url == "" or save_location == "":
            QMessageBox.warning(self, " Data Error", "Provide URL or Save location")
        else:
            try:
                video = pafy.new(video_url)
                # create an pafy object
                video_stream = video.streams
                # A list of regular streams (both audio and video)
                video_quality = self.comboBox.currentIndex()
                # get quality of video
                if video_quality != -1:
                    # check if user choose a quality
                    video_name = video.title
                    extension = video_stream[video_quality].extension
                    full_name = self.generate_filename(video_name, extension)
                    # make name of video file
                    final_path_with_file_name = self.get_file_name_for_saving(save_location, full_name)
                    # make path of video name
                    video_stream[video_quality].download(filepath=final_path_with_file_name,
                                                         callback=self.Video_Progress)
                    # download video with specific quality choosing by user
                    QMessageBox.information(self, "Successful", "Your Download is be done")

            except:
                QMessageBox.warning(self, " Data Error", "SomeThing Wrong")

        self.Video_URL.setText("")
        self.Save_Video.setText("")
        self.progressBar_2.setValue(0)

    def Video_Progress(self, total, received, ratio, rate, time):
        read_data = received
        if total > 0:
            download_percentage = read_data * 100 / total
            self.progressBar_2.setValue(download_percentage)
            remaining_time = round(time // 60, 2)
            self.time_lable.setText(str("{} minutes remaining".format(remaining_time)))

    def Save_Browser(self):
        save_location = QFileDialog.getExistingDirectory(self, "Select Download Directory")

        self.Save_Video.setText(str(save_location))

    ######################
    # YouTub playlist    #
    ######################

    def Playlist_Downloads(self):
        playlist_url = self.Playlist_URL.text()
        save_location = self.Save_Playlist.text()
        if playlist_url == "" or save_location == "":
            QMessageBox.warning(self, " Data Error", "Please, Provide URL or Save location")
        else:
            try:
                playlist = get_playlist(playlist_url)
                # return a dict containing metadata and Pafy objects as listed in the YouTube playlist.
                playlist_video = playlist['items']
                # a list of dicts with each dict representing a video
                self.lcdNumber_2.display(len(playlist_video))
                os.chdir(save_location)
                if os.path.exists(str(playlist["title"])):
                    os.chdir(str(playlist["title"]))
                else:
                    os.mkdir(str(playlist["title"]))
                    os.chdir(str(playlist["title"]))
            except Exception as e:
                QMessageBox.warning(self, " Data Error", "Something Wrong")
            current_video_in_download = 1
        try:
            self.lcdNumber.display(current_video_in_download)
            QApplication.processEvents()
            for video in playlist_video:
                current_video = video["pafy"]
                current_video_stream = current_video.getbest()
                # return stream with the highest resolution (video and audio)
                current_video_stream.download(callback=self.PlayList_progress, remux_audio=True)
                # download playlist
                self.lcdNumber.display(current_video_in_download)
                QApplication.processEvents()
                current_video_in_download += 1
            QMessageBox.information(self, "Successful", "Your Download is be done")
            self.Playlist_URL.setText("")
            self.Save_Playlist.setText("")
            self.progressBar_3.setValue(0)
        except Exception:
            QMessageBox.warning(self, " Data Error", "Something Wrong")

    def PlayList_progress(self, total, received, ratio, rate, time):
        read_data = received
        if total > 0:
            download_percentage = read_data * 100 / total
            self.progressBar_3.setValue(download_percentage)
            remaining_time = round(time // 60, 2)
            QApplication.processEvents()
            self.labeltime.setText(str("{} minutes remaining".format(remaining_time)))

    def PlayList_Save(self):
        playlist_save_browse = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        self.Save_Playlist.setText(playlist_save_browse)

    ####################
    # social Downloads #
    ####################

    def Download_Social_Video(self):
        download_url = self.social_url.text()
        save_location = self.Save_SocialVideo.text()
        if download_url == "" or save_location == "":
            QMessageBox.warning(self, " Data Error", "Please, Provide URL or Save location")
        else:
            try:
                os.chdir(save_location)
                # change directory
                run(["you-get " + str(download_url)],
                    text=True, shell=True)
                # here i use tiny command-line is You-Get to download media contents
                # so i use The run() function to Run the command line, this function
                # form subprocesses module>
                QMessageBox.information(self, "Successful", "Your Download is be done")
            except Exception:
                QMessageBox.warning(self, " Data Error", "Please, Provide a valid URL or Save locations")

        self.Save_file.setText("")
        self.File_url.setText("")

    def Save_Social_Video(self):
        save_location = QFileDialog.getExistingDirectory(self, "Select Download Directory")

        self.Save_SocialVideo.setText(str(save_location))

    #########################
    # Processing on Videos  #
    #########################

    def Convert_from_Video_to_Audio(self):
        try:
            video = self.convert_video.text()
            # get path of video
            video_list = str(video).split("/")
            ext = str(video_list[-1].split(".")[-1])
            # get extension of video
            v = str(video).split("/")[-1].replace(ext, "mp3")
            # generate a name of audio
            audio = self.convert_audio.text()
            # get path to save audio file
            a = str(audio + "/" + v)
            if os.path.exists(a):
                split = a.split(".")
                audio_file = ".".join(split[:-1]) + "new." + split[-1]
                video_clip = VideoFileClip(video)
                # clip read from a video file
                audio_clip = video_clip.audio
                #  get the audio track of an already created video clip
                audio_clip.write_audiofile(audio_file)
                audio_clip.close()
            else:
                video_clip = VideoFileClip(video)
                # clip read from a video file
                audio_clip = video_clip.audio
                #  get the audio track of an already created video clip
                audio_clip.write_audiofile(a)
                audio_clip.close()
            QMessageBox.information(self, "Successful", "Your Process is be done")
            self.convert_video.setText("")
            self.convert_audio.setText("")
        except:
            QMessageBox.warning(self, " Data Error", "Please, Choose A Video")

    def Convert_Video_Browse(self):
        video = QFileDialog.getOpenFileName(self, caption="Open Video",
                                            directory=".", filter="All Files(*.*)")
        self.convert_video.setText(str(video[0]))

    def Convert_Audio_Browse(self):
        Audio = QFileDialog.getExistingDirectory(self, "Select Convert Directory")

        self.convert_audio.setText(str(Audio))

    def Merge_Video_and_Audio(self):
        try:
            video = self.merge_video.text()
            # get video path
            audio = self.merge_audio.text()
            # get audio path
            save_video = self.Merge_SaveBrowse.text()
            # get location to save video
            video_list = str(video).split("/")
            title = str(video_list[-1].split(".")[0])
            # title of video
            merge_video = str(save_video + "/" + title + ".webm")
            video_clip = VideoFileClip(video)
            # clip read from a video file
            audio_clip = AudioFileClip(audio)
            # clip read from a audio file
            video_clip = video_clip.set_audio(audio_clip)
            # export assign an audio clip as the soundtrack of a video clip
            video_clip.write_videofile(merge_video)
            video_clip.close()
            QMessageBox.information(self, "Successful", "Your Process is be done")
            self.merge_video.setText("")
            self.merge_audio.setText("")
            self.Merge_SaveBrowse.setText("")
        except Exception:
            QMessageBox.warning(self, " Data Error", "Please, Choose A Video or Audio")

    def Merge_Video_Browse(self):
        video = QFileDialog.getOpenFileName(self, caption="Open Video",
                                            directory=".", filter="All Files(*.*)")
        self.merge_video.setText(str(video[0]))

    def Merge_Audio_Browse(self):
        audio = QFileDialog.getOpenFileName(self, caption="Open Video",
                                            directory=".", filter="All Files(*.*)")
        self.merge_audio.setText(str(audio[0]))

    def Merge_Browse(self):
        save = QFileDialog.getExistingDirectory(self, "Select Convert Directory")

        self.Merge_SaveBrowse.setText(str(save))

    def Open_Home(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Download(self):
        self.tabWidget.setCurrentIndex(1)

    def Open_YouTub(self):
        self.tabWidget.setCurrentIndex(2)

    def Open_Social(self):
        self.tabWidget.setCurrentIndex(3)

    def Open_Convert(self):
        self.tabWidget.setCurrentIndex(4)

    def Move_Box_1(self):
        box_animation1 = QPropertyAnimation(self.groupBox, b"geometry")
        box_animation1.setDuration(2500)
        box_animation1.setStartValue(QRect(0, 0, 0, 0))
        box_animation1.setEndValue(QRect(20, 30, 211, 211))
        box_animation1.start()
        self.box_animation1 = box_animation1

    def Move_Box_2(self):
        box_animation2 = QPropertyAnimation(self.groupBox_2, b"geometry")
        box_animation2.setDuration(2500)
        box_animation2.setStartValue(QRect(0, 0, 0, 0))
        box_animation2.setEndValue(QRect(320, 20, 221, 211))
        box_animation2.start()
        self.box_animation2 = box_animation2

    def Move_Box_3(self):
        box_animation3 = QPropertyAnimation(self.groupBox_3, b"geometry")
        box_animation3.setDuration(2500)
        box_animation3.setStartValue(QRect(0, 0, 0, 0))
        box_animation3.setEndValue(QRect(20, 250, 241, 201))
        box_animation3.start()
        self.box_animation3 = box_animation3

    def Move_Box_4(self):
        box_animation4 = QPropertyAnimation(self.groupBox_4, b"geometry")
        box_animation4.setDuration(2500)
        box_animation4.setStartValue(QRect(0, 0, 0, 0))
        box_animation4.setEndValue(QRect(320, 250, 231, 211))
        box_animation4.start()
        self.box_animation4 = box_animation4


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
