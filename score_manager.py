import json
import os
import pygame

LEADERBOARD_FILE="leaderboard.json"
leaderboard=pygame.image.load('image/high_score.png')
leaderboard=pygame.transform.scale(leaderboard,(570,650))
def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE,"r") as f:
                data=json.load(f)
                return sorted(data,reverse=True)
        except:
            return[]
    return[]
def save_score_to_leaderboard(new_score):
    score=load_leaderboard()
    if new_score>0:
        score.append(int(new_score))
        score=sorted(score,reverse=True)[:5]
        with open(LEADERBOARD_FILE,"w") as f:
            json.dump(score,f)
def get_highest_score():
    score=load_leaderboard()
    return score[0] if score else 0
def draw_leaderboard(screen,menu_bg,clock,fps):
    run_lb= True
    score=load_leaderboard()
    screen_width=screen.get_width()

    while run_lb:
        screen.blit(menu_bg,(0,0))
        screen.blit(leaderboard, (220, -50))
        font_title=pygame.font.Font("font/Coiny-Regular.ttf",48)
        title_surf=font_title.render("BẢNG XẾP HẠNG",True,(0,0,0))
        screen.blit(title_surf,(screen_width//2-title_surf.get_width()//2,150))
        font_score=pygame.font.Font("font/Coiny-Regular.ttf",32)
        if not score:
            empty_surf=font_score.render("Chưa có kỷ lục nào",True,(255,255,255))
            screen.blit(empty_surf,(screen_width//2-empty_surf.get_width()//2,260))
        else:
            for idx,sc in enumerate(score):
                text=f"Top {idx+1}: {sc} điểm"
                color=(255,255,0) if idx==0 else (255,255,255)
                score_surf=font_score.render(text,True,color)
                screen.blit(score_surf,(screen_width//2-score_surf.get_width()//2,240+idx*50))
        font_back=pygame.font.Font("font/Coiny-Regular.ttf",24)
        back_surf=font_back.render("Nhấn ESC để quay về menu",True,(255,255,255))
        screen.blit(back_surf,(screen_width//2-back_surf.get_width()//2,500))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    run_lb=False
        pygame.display.update()
        clock.tick(fps)
