import cv2
import pygame

class Video:
    def __init__(self, path_video, path_audio) -> None:
        self.video = cv2.VideoCapture(path_video)
        self.path_audio = path_audio
        self.frame = 0
        self.video_ended = False
    
    def play_audio(self, mixer):
        mixer.music.load(self.path_audio)
        mixer.music.play()
    
    def play_video(self, screen):
        if not self.video_ended:
            if self.frame % 2 == 0:
                stream, video_image = self.video.read()
                if stream:
                    video_surf = pygame.image.frombuffer(
                        video_image.tobytes(), video_image.shape[1::-1], 'BGR')
                    screen.blit(video_surf, (0, 150))
                else:
                    self.video_ended = True
            self.frame += 1                    
        return self.video_ended
                