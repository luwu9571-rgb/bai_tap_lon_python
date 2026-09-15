import random

import pygame
from pygame import mixer
from pygame.locals import *

from maps import map_list

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock=pygame.time.Clock()
fps=60
current_bgm=None

screen_width = 1024
screen_height = 768
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Platformer')

tile_size=32
game_over=0
dead_screen_alpha=0
main_menu=True
paused=False
in_tutorial=False
score=0
high_score=0
font=pygame.font.SysFont('Arial',28,bold=True)
cannon_group=pygame.sprite.Group()
bullet_group=pygame.sprite.Group()
coin_group=pygame.sprite.Group()
trap_down_group=pygame.sprite.Group()

menu_bg=pygame.image.load('image/Background1.png')
bg_img=pygame.image.load('image/Background.png')
restart_img=pygame.image.load('image/restart_button.png')
main_menu_img=pygame.image.load('image/menu_button.png')
dead_screen_img=pygame.image.load('image/dead_screen.png')
restart_hover_img=pygame.image.load('image/replay_point.png')
menu_hover_img=pygame.image.load('image/menu_point.png')
play_button=pygame.image.load('image/play_button.png')
how_to_play_button=pygame.image.load('image/how_to_play_button.png')
high_score_button=pygame.image.load('image/high_score_button.png')
quit_button=pygame.image.load('image/quit_button.png')
quit_hover=pygame.image.load('image/quit_hover.png')
play_hover=pygame.image.load('image/play_hover.png')
high_score_hover=pygame.image.load('image/high_score_hover.png')
how_to_play_hover=pygame.image.load('image/how_to_play_hover.png')
continue_button=pygame.image.load('image/continue_button.png')
continue_hover=pygame.image.load('image/continue_hover.png')
continue_button=pygame.transform.scale(continue_button,(tile_size*6,tile_size*2.5))
continue_hover=pygame.transform.scale(continue_hover,(tile_size*6,tile_size*2.5))
play_button=pygame.transform.scale(play_button,(tile_size*6,tile_size*2.5))
how_to_play_button=pygame.transform.scale(how_to_play_button,(tile_size*6,tile_size*2.5))
high_score_button=pygame.transform.scale(high_score_button,(tile_size*6,tile_size*2.5))
quit_button=pygame.transform.scale(quit_button,(tile_size*6,tile_size*2.5))
dead_screen_img=pygame.transform.scale(dead_screen_img,(screen_width,screen_height))
restart_img=pygame.transform.scale(restart_img,(tile_size*6,tile_size*2.5))
main_menu_img=pygame.transform.scale(main_menu_img,(tile_size*6,tile_size*2.5))
restart_hover_img=pygame.transform.scale(restart_hover_img,(tile_size*6,tile_size*2.5))
menu_hover_img=pygame.transform.scale(menu_hover_img,(tile_size*6,tile_size*2.5))
bg_img = pygame.transform.scale(bg_img,(screen_width,screen_height))
menu_bg = pygame.transform.scale(menu_bg,(screen_width,screen_height))
play_hover=pygame.transform.scale(play_hover,(tile_size*6,tile_size*2.5))
high_score_hover=pygame.transform.scale(high_score_hover,(tile_size*6,tile_size*2.5))
how_to_play_hover=pygame.transform.scale(how_to_play_hover,(tile_size*6,tile_size*2.5))
quit_hover=pygame.transform.scale(quit_hover,(tile_size*6,tile_size*2.5))

coin_sf=pygame.mixer.Sound('sound/coin.wav')
coin_sf.set_volume(0.3)
jump_sf=pygame.mixer.Sound('sound/jump.wav')
jump_sf.set_volume(0.3)
dash_sf=pygame.mixer.Sound('sound/dash.wav')
dash_sf.set_volume(0.3)
explosion_sf=pygame.mixer.Sound('sound/explosion.wav')
explosion_sf.set_volume(0.1)
bounce_sf=pygame.mixer.Sound('sound/bounce.wav')
bounce_sf.set_volume(0.5)
monster_scream_sf=pygame.mixer.Sound('sound/monster_scream.wav')
monster_scream_sf.set_volume(1)
game_over_sf=pygame.mixer.Sound('sound/game_over.wav')
game_over_sf.set_volume(0.5)
click_button_sf=pygame.mixer.Sound('sound/click_button.wav')
click_button_sf.set_volume(0.5)
def draw_grid():
    for line in range(0,16):
        pygame.draw.line(screen,(255,255,255),(0,line * tile_size),(screen_width,line*tile_size),2)
        pygame.draw.line(screen,(255,255,255),(line*tile_size,0),(line*tile_size,screen_height),2)

def play_bgm(music_file,volume=0.5):
    global current_bgm
    if current_bgm !=music_file:
        current_bgm=music_file
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)


class monster(pygame.sprite.Sprite):
    def __init__(self,x,screen_height,num_frame=40,monster_width=800,speed=1.5,anim_speed=1):
        super().__init__()
        self.speed=speed
        self.base_speed=speed
        self.max_speed=3
        self.speed_increase=0.00015
        sheet=pygame.image.load('image/monster.png')
        frame_width=sheet.get_width()//num_frame
        frame_height=sheet.get_height()
        self.frame=[]
        for i in range(num_frame):
            frame=sheet.subsurface((i*frame_width,0,frame_width,frame_height))
            bouding_box=frame.get_bounding_rect()
            cropped_frame=frame.subsurface(bouding_box)
            scale_frame=pygame.transform.scale(cropped_frame,(monster_width,screen_height))
            self.frame.append(scale_frame)
        self.current_frame=0
        self.anim_speed=anim_speed
        self.image=self.frame[int(self.current_frame)]
        self.rect=self.image.get_rect(topleft=(x,0))
        self.hitbox=self.rect.copy()
    def update(self,player):
        if self.speed<self.max_speed:
            self.speed+=self.speed_increase
            if self.speed>self.max_speed:
                self.speed=self.max_speed
                print("max_speed")
        curent_distance=player.rect.x-self.rect.x
        if curent_distance>1200:
            current_speed=self.speed*5
        else:
            current_speed=self.speed
        self.rect.x+=current_speed
        self.hitbox.center=self.rect.center
        self.current_frame+=self.anim_speed
        if self.current_frame>=len(self.frame):
            self.current_frame=0
        self.image=self.frame[int(self.current_frame)]
        if self.hitbox.colliderect(player.hitbox):
            return -1
        return 0
    def draw(self,surface,camera):
        render_pos=(self.rect.x-camera.offset.x,0)
        surface.blit(self.image,render_pos)


class endlessworld():
    def __init__(self,tile_size):
        self.tile_size=tile_size
        self.grass_img=pygame.image.load('image/grass.png')
        self.dirt_img=pygame.image.load('image/dirt.png')
        self.platform_single_img=pygame.image.load('image/platform_single.png')
        self.platform_row_left_img=pygame.image.load('image/platform_row_left.png')
        self.platform_row_right_img=pygame.image.load('image/platform_row_right.png')
        self.platform_row_mid_img=pygame.image.load('image/platform_row_mid.png')
        self.platform_col_mid_img=pygame.image.load('image/platform_col_mid.png')
        self.platform_col_top_img=pygame.image.load('image/platform_col_top.png')
        self.platform_col_bot_img=pygame.image.load('image/platform_col_bot.png')
        self.room_cols=len(map_list[0][0])
        self.room_width=self.room_cols*tile_size
        self.random_map_list=map_list[1:]
        self.active_room=[
            map_list[0],
            random.choice(self.random_map_list),
            random.choice(self.random_map_list),
        ]
        self.tile_list=[]
        self.coin_group = pygame.sprite.Group()
        self.trap_down_group = pygame.sprite.Group()
        self.build_combined_world()
        for room_idx, room_data in enumerate(self.active_room):
            self.spawn_entities(room_data,room_idx)
    def spawn_entities(self,room_data,room_idx):
        offset_x=room_idx*self.room_width
        for row_count, row in enumerate(room_data):
            for col_count, tile in enumerate(row):
                x = offset_x + (col_count * self.tile_size)
                y = row_count * self.tile_size
                if tile==10:
                    coin=Coin(x,y,size=24,num_frame=4,anim_speed=0.2)
                    self.coin_group.add(coin)
                elif tile==15:
                    trap_down=Trap_down(x,y)
                    self.trap_down_group.add(trap_down)

    def build_combined_world(self):
        self.tile_list.clear()
        trap_group.empty()
        mushroom_group.empty()
        cannon_group.empty()
        bullet_group.empty()
        for room_idx,room_data in enumerate(self.active_room):
            offset_x=room_idx*self.room_width

            row_count=0
            for row in room_data:
                col_count=0
                for tile in row:
                    x=offset_x+(col_count*self.tile_size)
                    y=row_count*self.tile_size
                    if tile==0:
                        pass
                    elif tile==1:
                        img = pygame.transform.scale(self.grass_img,(self.tile_size,self.tile_size))
                        img_rect=img.get_rect()
                        img_rect.x = x
                        img_rect.y = y
                        self.tile_list.append((img,img_rect))
                    elif tile==2:
                        img= pygame.transform.scale(self.dirt_img,(self.tile_size,self.tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = x
                        img_rect.y = y
                        self.tile_list.append((img, img_rect))
                    elif tile==3:
                        img = pygame.transform.scale(self.platform_row_left_img, (self.tile_size, self.tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = x
                        img_rect.y = y
                        self.tile_list.append((img, img_rect))
                    elif tile==4:
                        img = pygame.transform.scale(self.platform_row_mid_img, (self.tile_size, self.tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = x
                        img_rect.y = y
                        self.tile_list.append((img, img_rect))
                    elif tile==5:
                        img = pygame.transform.scale(self.platform_row_right_img, (self.tile_size, self.tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = x
                        img_rect.y = y
                        self.tile_list.append((img, img_rect))
                    elif tile==11:
                        img = pygame.transform.scale(self.platform_col_bot_img, (self.tile_size, self.tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = x
                        img_rect.y = y
                        self.tile_list.append((img, img_rect))
                    elif tile==12:
                        img = pygame.transform.scale(self.platform_col_mid_img, (self.tile_size, self.tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = x
                        img_rect.y = y
                        self.tile_list.append((img, img_rect))
                    elif tile==13:
                        img = pygame.transform.scale(self.platform_col_top_img, (self.tile_size, self.tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = x
                        img_rect.y = y
                        self.tile_list.append((img, img_rect))
                    elif tile==14:
                        img = pygame.transform.scale(self.platform_single_img, (self.tile_size, self.tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = x
                        img_rect.y = y
                        self.tile_list.append((img, img_rect))
                    elif tile==6:
                        trap=Trap(x,y)
                        trap_group.add(trap)
                    elif tile == 7:
                        mushroom = Mushroom(x, y, tile_size, bounce_force=-16)
                        mushroom_group.add(mushroom)
                    elif tile == 8:
                        cannon = Cannon(x, y, tile_size, direction="left",shoot_cooldown=90)
                        cannon_group.add(cannon)
                    elif tile == 9:
                        cannon = Cannon(x, y, tile_size, direction="right",shoot_cooldown=90)
                        cannon_group.add(cannon)


                    col_count+=1
                row_count+=1
    def update(self,player,camera,chaser_monster=None):
        if player.hitbox.x>=2*self.room_width:
            self.active_room.pop(0)
            new_room=random.choice(self.random_map_list)
            self.active_room.append(new_room)
            player.rect.x-=self.room_width
            player.hitbox.x-=self.room_width
            camera.offset.x-=self.room_width
            if chaser_monster:
                chaser_monster.rect.x-=self.room_width
                chaser_monster.hitbox.x-=self.room_width
            for coin in self.coin_group:
                coin.rect.x-=self.room_width
            for trap in trap_group:
                trap.rect.x -= self.room_width
            for trap_down in self.trap_down_group:
                trap_down.rect.x -= self.room_width
                trap_down.hitbox.x -= self.room_width
            for shroom in mushroom_group:
                shroom.rect.x -= self.room_width
            for cannon in cannon_group:
                cannon.rect.x -= self.room_width
            self.spawn_entities(new_room,room_idx=2)

            self.build_combined_world()
    def reset_world(self):
        self.active_room=[
            map_list[0],
            random.choice(self.random_map_list),
            random.choice(self.random_map_list)
        ]
        self.coin_group.empty()
        trap_group.empty()
        self.trap_down_group.empty()
        mushroom_group.empty()
        cannon_group.empty()
        bullet_group.empty()
        self.build_combined_world()
        for room_idx, room_data in enumerate(self.active_room):
            self.spawn_entities(room_data,room_idx)

    def draw(self,surface,camera):
        for tile in self.tile_list:
            surface.blit(tile[0],camera.apply(tile[1]))

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,speed_x,speed_y=0):
        super().__init__()
        bullet_img=pygame.image.load('image/bullet.png')
        self.image=pygame.transform.scale(bullet_img,(16,16))
        if speed_x<0:
            self.image=pygame.transform.flip(self.image,True,False)
        self.rect=self.image.get_rect(center=(x,y))
        self.hitbox=self.rect.copy()
        self.speed_x=speed_x
        self.speed_y=speed_y
        self.distance_fly=0
        self.max_distance=500
    def update(self,world,player):
        self.rect.x+=self.speed_x
        self.rect.y+=self.speed_y
        self.hitbox.center=self.rect.center
        self.distance_fly+=abs(self.speed_x)+abs(self.speed_y)
        if self.distance_fly>self.max_distance:
            self.kill()
            return 0

        if self.hitbox.colliderect(player.hitbox):
            return -1
        for tile in world.tile_list:
            if tile[1].colliderect(self.hitbox):
                self.kill()
                break
        return 0

class Cannon(pygame.sprite.Sprite):
    def __init__(self,x,y,tile_size,direction="left",shoot_cooldown=120,bullet_speed=5):
        super().__init__()
        self.tile_size=tile_size
        self.direction=direction
        self.shoot_cooldown=shoot_cooldown
        self.cooldown_time=0
        self.bullet_speed=bullet_speed
        sheet=pygame.image.load('image/cannon.png').convert_alpha()
        num_frames=8
        frame_width=sheet.get_width()//num_frames
        frame_height=sheet.get_height()
        self.frames=[]
        for i in range(num_frames):
            frame=sheet.subsurface((i*frame_width,0,frame_width,frame_height))
            scaled_frame=pygame.transform.scale(frame,(tile_size*1.5,tile_size+7))
            if self.direction=="left":
                scaled_frame=pygame.transform.flip(scaled_frame,True,False)
            self.frames.append(scaled_frame)
        self.current_frame=0
        self.image=self.frames[self.current_frame]
        self.rect=self.image.get_rect(topleft=(x,y))
        self.is_shooting=False
        self.anim_speed=0.2
        self.anim_time=0
    def update(self,bullet_group):
        self.cooldown_time+=1
        if self.cooldown_time>=self.shoot_cooldown:
            self.cooldown_time=0
            explosion_sf.play()
            self.trigger_shoot(bullet_group)
        if self.is_shooting:
            self.anim_time+=self.anim_speed
            if self.anim_time>=1:
                self.anim_time=0
                self.current_frame+=1
                if self.current_frame>=len(self.frames):
                    self.current_frame=0
                    self.is_shooting=False
            self.image=self.frames[int(self.current_frame)]
    def trigger_shoot(self,bullet_group):
        self.is_shooting=True
        self.current_frame=0
        self.anim_time=0
        vx,vy=0,0
        spawn_x,spawn_y=self.rect.centerx,self.rect.centery
        if self.direction=="left":
            vx=-self.bullet_speed
            spawn_x=self.rect.left
        elif self.direction=="right":
            vx=self.bullet_speed
            spawn_x=self.rect.right
        bullet=Bullet(spawn_x,spawn_y,vx,vy)
        bullet_group.add(bullet)

class Ghost():
    def __init__(self,x,y,image):
        self.x=x
        self.y=y
        self.image=image.copy()
        self.alpha=200
        self.fade_speed=25
    def update(self):
        self.alpha-=self.fade_speed
        if self.alpha<0:
            self.alpha=0
    def draw(self,surface):
        self.image.set_alpha(self.alpha)
        surface.blit(self.image,(self.x,self.y))

class Trap(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('image/trap.png')
        self.image=pygame.transform.scale(img,(tile_size,tile_size))
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

        self.hitbox=pygame.Rect(0,0,tile_size-10,tile_size-10)
        self.hitbox.midbottom=self.rect.midbottom
    def update(self,world_shift):
        self.rect+=world_shift


class Trap_down(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('image/trap_down.png')
        self.image=pygame.transform.scale(img,(tile_size,tile_size))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.chance=0.5
        self.vel_y=0
        self.isfalling=False
        self.hitbox=pygame.Rect(0,0,tile_size,tile_size)
        self.hitbox.midbottom=self.rect.midbottom
    def fall(self):
        if not self.isfalling:
            if random.random()<self.chance:
                self.isfalling=True
    def update(self,world):
        if self.isfalling:
            self.vel_y+=0.7
            if self.vel_y>6:
                self.vel_y=6
            self.rect.y+=self.vel_y
            self.hitbox.midbottom=self.rect.midbottom
            for img,tile_rect in world.tile_list:
                if tile_rect.colliderect(self.hitbox):
                    self.kill()
                    break

class Camera:
    def __init__(self,width,height,deadzone_width=250):
        self.offset=pygame.Vector2(0,0)
        self.screen_width=width
        self.screen_height=height

        self.deadzone_width=deadzone_width
        self.deadzone_left=(self.screen_width-self.deadzone_width)//2
        self.deadzone_right=(self.screen_width+self.deadzone_width)//2

        self.shake_amount=0
        self.shake_time=0
        self.shake_offset_x=0
        self.shake_offset_y=0
        self.time_couter=0
        self.heavy_shake_time=200
        self.heavy_shake_chance=0.4

    def trigger_shake(self,intensity,duration):
        self.shake_amount=intensity
        self.shake_time=duration

    def update(self,target_rect,shake_enable=True):
        player_screen_x=target_rect.centerx - self.offset.x

        if player_screen_x>self.deadzone_right:
            self.offset.x+=player_screen_x-self.deadzone_right
        elif player_screen_x<self.deadzone_left:
            self.offset.x+=player_screen_x-self.deadzone_left
        self.offset.y=0
        if shake_enable:
            if self.shake_time>0:
                self.shake_time-=1
            else:
                self.shake_amount=1
            self.time_couter+=1
            if self.time_couter>=self.heavy_shake_time:
                self.time_couter=0
                if random.random()<self.heavy_shake_chance:
                    for Trap_down in endlessworld.trap_down_group:
                        Trap_down.fall()
                    monster_scream_sf.play()
                    self.trigger_shake(intensity=6,duration=70)
            if self.shake_amount>0:
                self.shake_offset_x = random.randint(-self.shake_amount,self.shake_amount)
                self.shake_offset_y = random.randint(-self.shake_amount, self.shake_amount)
            else:
                self.shake_offset_x=0
                self.shake_offset_y=0
        else:
            self.shake_offset_x=0
            self.shake_offset_y=0
            self.shake_time=0
            self.shake_amount=0

    def apply(self,rect):
        return rect.move(-int(self.offset.x)+self.shake_offset_x,-int(self.offset.y)+self.shake_offset_y)

class button():
    def __init__(self,x,y,image,hover_image=None):
        self.image=image
        self.hover_image=hover_image if hover_image else image
        self.rect = self.image.get_rect()
        self.rect.center=(x,y)
        self.clicked=False

    def draw(self):
        action=False
        pos=pygame.mouse.get_pos()
        current_img=self.image

        if self.rect.collidepoint(pos):
            current_img=self.hover_image

            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
                click_button_sf.play()
                action=True
                self.clicked=True

        if pygame.mouse.get_pressed()[0]==0:
            self.clicked=False

        screen.blit(current_img,self.rect)

        return action

pause_overlayer=pygame.Surface((screen_width,screen_height))
pause_overlayer.set_alpha(150)
pause_overlayer.fill((0,0,0))
def draw_pause_screen():
    screen.blit(pause_overlayer,(0,0))

    if continue_button.draw():
        return "continue"
    if pause_menu_button.draw():
        return "pause_main"
    if pause_restart_button.draw():
        return "pause_restart"
    return None

def draw_score(surface,score):
    score_text=font.render(f"Score: {int(score)}",True,(255,255,255))
    surface.blit(score_text,(20,20))

class Mushroom(pygame.sprite.Sprite):
    def __init__(self,x,y,tile_size,bounce_force=-16):
        super().__init__()
        self.tile_size=tile_size
        self.bounce_force=bounce_force

        sheet=pygame.image.load('image/shroom.png').convert_alpha()
        frame_width=sheet.get_width()/4
        frame_height=sheet.get_height()
        self.frames=[]
        for i in range(4):
            frame=sheet.subsurface((i*frame_width,0,frame_width,frame_height))
            scaled_frame=pygame.transform.scale(frame,(tile_size*2,tile_size*2))
            self.frames.append(scaled_frame)
        self.current_frame=0
        self.image=self.frames[self.current_frame]
        offset_x=tile_size//2
        offset_y=tile_size
        self.rect=self.image.get_rect()
        self.rect.x=x-offset_x
        self.rect.y=y-offset_y+10
        hitbox_w=int(tile_size*2*0.6)
        hitbox_h=int(tile_size*2*0.6)
        self.hitbox=pygame.Rect(0,0,hitbox_w,hitbox_h)
        self.hitbox.midbottom=self.rect.midbottom
        self.is_bouncing=False
        self.anim_speed=0.2
        self.anim_timer=0
    def trigger_bounce(self,player):
        player.vel_y=self.bounce_force
        player.in_air=True
        player.jump_count=1
        player.can_dash=True

        self.is_bouncing=True
        self.current_frame=0
        self.anim_timer=0
    def update(self,player):
        if self.hitbox.colliderect(player.hitbox):
            if player.vel_y>0 and player.hitbox.bottom<=self.hitbox.centery+10:
                bounce_sf.play()
                player.hitbox.bottom=self.hitbox.top
                self.trigger_bounce(player)
        if self.is_bouncing==True:
            self.anim_timer+=self.anim_speed
            if self.anim_timer>=1:
                self.anim_timer=0
                self.current_frame+=1
                if self.current_frame>=len(self.frames):
                    self.current_frame=0
                    self.is_bouncing=False
            self.image=self.frames[int(self.current_frame)]

class Coin(pygame.sprite.Sprite):
    def __init__(self,x,y,size=24,num_frame=4,anim_speed=0.2):
        super().__init__()
        self.anim_speed=anim_speed
        sheet=pygame.image.load('image/Coin.png').convert_alpha()
        frame_width=sheet.get_width()//num_frame
        frame_height=sheet.get_height()
        self.frames=[]
        for i in range(num_frame):
            frame=sheet.subsurface((i*frame_width,0,frame_width,frame_height))
            scaled_frame=pygame.transform.scale(frame,(size,size))
            self.frames.append(scaled_frame)
        self.current_frame=0
        self.image=self.frames[int(self.current_frame)]
        self.rect=self.image.get_rect(topleft=(x,y))
    def update(self,player):
        self.current_frame+=self.anim_speed
        if self.current_frame>=len(self.frames):
            self.current_frame=0
        self.image=self.frames[int(self.current_frame)]
        if self.rect.colliderect(player.hitbox):
            self.kill()
            coin_sf.play()
            return True
        return False


class Player():
    def __init__(self,x,y):
        self.reset(x,y)

    def draw(self,surface,camera):
        for ghost in self.ghosts:
            ghost.image.set_alpha(ghost.alpha)
            surface.blit(ghost.image,camera.apply(pygame.Rect(ghost.x,ghost.y,64,64)))

        surface.blit(self.image,camera.apply(self.rect))

    def update(self, world, game_over):
        tile_list=world.tile_list if hasattr(world,'tile_list') else world
        dx=0
        dy=0
        walk_cooldown=5

        if game_over==0:
            key=pygame.key.get_pressed()

            input_x=0
            input_y=0
            if key[pygame.K_a]:
                input_x-=1
                self.direction=-1
            if key[pygame.K_d]:
                input_x+=1
                self.direction=1
            if key[pygame.K_w]:
                input_y-=1
            if key[pygame.K_s]:
                input_y+=1

            if self.dash_cooldown_time>0:
                self.dash_cooldown_time -= 1
            if key[pygame.K_LSHIFT] and self.can_dash and self.dash_cooldown_time==0:
                self.is_dashing=True
                self.can_dash=False
                dash_sf.play()
                self.dash_time=self.dash_duration
                self.dash_cooldown_time=self.dash_cooldown
                self.dash_dir=self.direction

            if self.is_dashing:
                self.dash_time -=1
                self.vel_y=0
                dx=self.dash_dir * self.dash_speed

                if self.ghost_spawn_cooldown<=0:
                    self.ghosts.append(Ghost(self.rect.x,self.rect.y,self.image))
                    self.ghost_spawn_cooldown=2
                else:
                    self.ghost_spawn_cooldown -= 1

                if self.dash_time<=0:
                    self.is_dashing=False

            else:
                if self.vel_x>0:
                    self.vel_x -=1
                elif self.vel_x<0:
                    self.vel_x +=1

                if key[pygame.K_a]:
                    dx -= 3
                    self.counter+=1
                    self.direction=-1
                if key[pygame.K_d]:
                    dx += 3
                    self.counter+=1
                    self.direction=1

                dx+=self.vel_x

                if key[pygame.K_a]==False and key[pygame.K_d]==False:
                    self.counter = 0
                    self.index = 0
                    self.image=self.image_right[self.index]

                if key[pygame.K_SPACE] and not self.jumped:
                    if self.on_wall and self.in_air:
                        jump_sf.play()
                        self.vel_y=-10
                        self.vel_x=-self.wall_direction*8
                        self.jumped=True
                        self.on_wall=False
                    elif self.jump_count<self.max_jump:
                        jump_sf.play()
                        self.vel_y=-10
                        self.jump_count+=1
                        self.jumped=True
                        self.in_air=True
                if not key[pygame.K_SPACE]:
                    self.jumped=False


                if self.direction==1:
                    self.image=self.image_right[self.index]
                elif self.direction==-1:
                    self.image=self.image_left[self.index]


            if self.counter>walk_cooldown:
                self.counter=0
                self.index+=1
                if self.index>=len(self.image_right):
                    self.index=0
                self.image=self.image_right[self.index]

            self.vel_y +=1
            if self.on_wall and self.vel_y>0:
                if self.vel_y>2:
                    self.vel_y =2
            else:
                if self.vel_y >7:
                    self.vel_y=7
            dy+=self.vel_y
            self.in_air=True
            self.on_wall=False

            for tile in world.tile_list:
                if tile[1].colliderect(self.hitbox.x + dx,self.hitbox.y,self.hitbox.width,self.hitbox.height):
                    if self.in_air:
                        self.on_wall=True
                        self.jump_count=0
                        self.can_dash=True
                        if dx>0:
                            self.wall_direction=1
                        elif dx<0:
                            self.wall_direction=-1
                    dx=0
                    if self.is_dashing:
                        self.is_dashing=False

                if tile[1].colliderect(self.hitbox.x ,self.hitbox.y + dy,self.hitbox.width,self.hitbox.height):
                    if self.vel_y < 0:
                        dy=tile[1].bottom - self.hitbox.top
                    elif self.vel_y >= 0:
                        dy=tile[1].top - self.hitbox.bottom
                    self.vel_y=0
                    self.in_air=False
                    self.jump_count=0
                    self.can_dash=True

            for trap in trap_group:
                if self.hitbox.colliderect(trap.hitbox):
                    game_over=-1
                    print("lmao")
            for trap_down in endlessworld.trap_down_group:
                if self.hitbox.colliderect(trap_down.hitbox):
                    game_over=-1
                    print("game_over")

            self.hitbox.x += dx
            self.hitbox.y += dy

            if self.hitbox.bottom > screen_height:
                self.hitbox.bottom=screen_height
                dy=0
                self.in_air=False

            y_offset=14
            self.rect.midbottom=self.hitbox.midbottom[0],self.hitbox.midbottom[1]+y_offset

            for ghost in self.ghosts[:]:
                ghost.update()
                if ghost.alpha<=0:
                    self.ghosts.remove(ghost)

        #pygame.draw.rect(screen,(255,255,255),self.hitbox,2)

        return game_over

    def reset(self,x,y):
        global dead_screen_alpha
        dead_screen_alpha=0

        self.image_right = []
        self.image_left = []
        self.index = 0
        self.counter = 0
        self.direction = 1
        player_sheet = pygame.image.load('image/player.png')

        for i in range(0, 6):
            player_frame = player_sheet.subsurface((32 + i * 128, 0, 64, 64))
            scaled_frames = pygame.transform.scale(player_frame, (64, 64))
            self.image_right.append(scaled_frames)
            fipped_frames = pygame.transform.flip(scaled_frames, True, False)
            self.image_left.append(fipped_frames)
        self.image = self.image_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.hight = self.image.get_height()

        hitbox_width = 24
        hitbox_height = 24
        self.hitbox = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.midbottom = self.rect.midbottom
        self.vel_y = 0
        self.vel_x = 0
        self.jumped = False
        self.in_air = True
        self.max_jump = 2
        self.jump_count = 0

        self.on_wall = False
        self.wall_direction = 0

        self.is_dashing = False
        self.can_dash = True
        self.dash_time = 0
        self.dash_cooldown_time = 0
        self.dash_speed = 12
        self.dash_duration = 10
        self.dash_cooldown = 24
        self.dash_dir = 1

        self.ghosts = []
        self.ghost_spawn_cooldown = 0

class World():
    def __init__(self,data):
        self.data = data
        self.text_list = []
        self.tile_list=[]
        self.coin_group=pygame.sprite.Group()
        self.grass_img=pygame.image.load('image/grass.png')
        self.dirt_img=pygame.image.load('image/dirt.png')
        self.platform_single_img = pygame.image.load('image/platform_single.png')
        self.platform_row_left_img = pygame.image.load('image/platform_row_left.png')
        self.platform_row_right_img = pygame.image.load('image/platform_row_right.png')
        self.platform_row_mid_img = pygame.image.load('image/platform_row_mid.png')
        self.platform_col_mid_img = pygame.image.load('image/platform_col_mid.png')
        self.platform_col_top_img = pygame.image.load('image/platform_col_top.png')
        self.platform_col_bot_img = pygame.image.load('image/platform_col_bot.png')
        self.build_world()
    def build_world(self):
        trap_group.empty()
        mushroom_group.empty()
        cannon_group.empty()
        bullet_group.empty()
        trap_down_group.empty()
        trap_down_group.empty()
        self.coin_group.empty()
        self.font = pygame.font.Font("font/Coiny-Regular.ttf", 18)
        row_count=0
        for row in self.data:
            col_count=0
            for tile in row:
                x_pos=col_count * tile_size
                y_pos=row_count * tile_size
                if tile ==0:
                    pass
                elif tile==1:
                    img=pygame.transform.scale(self.grass_img,(tile_size,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x=col_count * (tile_size)
                    img_rect.y=row_count * (tile_size)
                    self.tile_list.append((img,img_rect))
                elif tile==2:
                    img=pygame.transform.scale(self.dirt_img,(tile_size,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x=col_count * (tile_size)
                    img_rect.y=row_count * (tile_size)
                    self.tile_list.append((img,img_rect))
                elif tile==3:
                    img=pygame.transform.scale(self.platform_row_left_img,(tile_size,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x=col_count * (tile_size)
                    img_rect.y=row_count * (tile_size)
                    self.tile_list.append((img,img_rect))
                elif tile==4:
                    img=pygame.transform.scale(self.platform_row_mid_img,(tile_size,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x=col_count * (tile_size)
                    img_rect.y=row_count * (tile_size)
                    self.tile_list.append((img,img_rect))
                elif tile==5:
                    img=pygame.transform.scale(self.platform_row_right_img,(tile_size,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x=col_count * (tile_size)
                    img_rect.y=row_count * (tile_size)
                    self.tile_list.append((img,img_rect))
                elif tile==11:
                    img=pygame.transform.scale(self.platform_col_bot_img,(tile_size,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x=col_count * (tile_size)
                    img_rect.y=row_count * (tile_size)
                    self.tile_list.append((img,img_rect))
                elif tile==12:
                    img=pygame.transform.scale(self.platform_col_mid_img,(tile_size,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x=col_count * (tile_size)
                    img_rect.y=row_count * (tile_size)
                    self.tile_list.append((img,img_rect))
                elif tile==13:
                    img=pygame.transform.scale(self.platform_col_top_img,(tile_size,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x=col_count * (tile_size)
                    img_rect.y=row_count * (tile_size)
                    self.tile_list.append((img,img_rect))
                elif tile==14:
                    img=pygame.transform.scale(self.platform_single_img,(tile_size,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x=col_count * (tile_size)
                    img_rect.y=row_count * (tile_size)
                    self.tile_list.append((img,img_rect))
                elif tile==6:
                    trap=Trap(col_count * tile_size,row_count * tile_size )
                    trap_group.add(trap)
                elif tile==15:
                    trap_down=Trap_down(col_count * tile_size,row_count * tile_size )
                    trap_down_group.add(trap_down)
                elif tile==7:
                    mushroom=Mushroom(col_count * tile_size,row_count * tile_size,tile_size,bounce_force=-16)
                    mushroom_group.add(mushroom)
                elif tile==8:
                    cannon=Cannon(col_count * tile_size,row_count * tile_size,tile_size,direction="left",shoot_cooldown=90)
                    cannon_group.add(cannon)
                elif tile==9:
                    cannon = Cannon(col_count * tile_size, row_count * tile_size, tile_size, direction="right",shoot_cooldown=90)
                    cannon_group.add(cannon)
                elif tile==10:
                    x = col_count * tile_size + (tile_size -24)//2
                    y = row_count * tile_size + (tile_size -24)//2
                    coin = Coin(x, y, size=24, num_frame=4, anim_speed=0.2)
                    self.coin_group.add(coin)

                elif tile==100:
                    txt=tutorial_text(x_pos,y_pos,"Nhấn A/D để di chuyển",self.font,trigger_distance=90)
                    self.text_list.append(txt)
                elif tile==101:
                    txt = tutorial_text(x_pos, y_pos, "Nhấn SPACE để nhảy", self.font, trigger_distance=100)
                    self.text_list.append(txt)
                elif tile==102:
                    txt = tutorial_text(x_pos, y_pos, "Bạn có thể nhấn SPACE 2 lần \n             để nhảy đôi", self.font, trigger_distance=80)
                    self.text_list.append(txt)
                elif tile==103:
                    txt = tutorial_text(x_pos, y_pos, "Nhấn L_SHIFT để lướt", self.font, trigger_distance=80)
                    self.text_list.append(txt)
                elif tile==104:
                    txt = tutorial_text(x_pos, y_pos, "Cẩn thận với các chướng ngại vật", self.font, trigger_distance=70)
                    self.text_list.append(txt)
                elif tile==105:
                    txt = tutorial_text(x_pos, y_pos, "                         Đừng lo !\nBạn đang ở chế độ hướng dẫn nên các\n      vật cản không thể gây hại cho bạn!", self.font, trigger_distance=120)
                    self.text_list.append(txt)
                elif tile==106:
                    txt = tutorial_text(x_pos, y_pos, "Thử nhảy lên cây nấm đi\n    Sẽ có điều bất ngờ", self.font, trigger_distance=140)
                    self.text_list.append(txt)
                elif tile==107:
                    txt = tutorial_text(x_pos, y_pos, "     Giữ bản thân sát tường\n ban có thể vào trạng thái trượt\n         và rơi chậm hơn", self.font, trigger_distance=140)
                    self.text_list.append(txt)
                elif tile==108:
                    txt = tutorial_text(x_pos, y_pos, "  Khi trong trạng thái trượt\nnhấn SPACE để bật lên 1 đoạn", self.font, trigger_distance=140)
                    self.text_list.append(txt)
                elif tile==109:
                    txt = tutorial_text(x_pos, y_pos, "Những viên đạn này có vẻ nguy hiểm\n     hãy cố gắng né chúng", self.font, trigger_distance=140)
                    self.text_list.append(txt)
                elif tile==110:
                    txt = tutorial_text(x_pos, y_pos, "Nhặt các đồng xu trong màn chạy\n         để nhận thêm điểm", self.font, trigger_distance=140)
                    self.text_list.append(txt)
                elif tile==111:
                    txt = tutorial_text(x_pos, y_pos, " Nhấn ESC để thoát về menu\ntrong màn chạy chính nhấn ESC\n       để tạm dừng game", self.font, trigger_distance=140)
                    self.text_list.append(txt)
                col_count+=1
            row_count+=1

    def draw(self,surface,camera):
        for tile in self.tile_list:
            surface.blit(tile[0],camera.apply(tile[1]))
        for coin in self.coin_group:
            surface.blit(coin.image, camera.apply(coin.rect))
        if player:
            for txt in self.text_list:
                txt.draw(surface,camera,player)
    def reset(self):
        self.build_world()

def draw_game_over_screen():
    global dead_screen_alpha
    if dead_screen_alpha<255:
        dead_screen_alpha+=5
        if dead_screen_alpha>255:
            dead_screen_alpha=255
    dead_screen_img.set_alpha(dead_screen_alpha)
    screen.blit(dead_screen_img,(0,0))
    if dead_screen_alpha>200:
        if restart_button.draw():
            return "restart"
        if main_menu_button.draw():
            return "main"

class tutorial_text:
    def __init__(self,x,y,text,font,color=(255,0,0),trigger_distance=50):
        self.x=x
        self.y=y
        self.text=text
        self.font=font
        self.color=color
        self.trigger_distance=trigger_distance
        self.surface=self.font.render(self.text,True,self.color)
        self.rect=self.surface.get_rect(center=(self.x,self.y))
    def draw(self,surface,camera,player):
        distance=abs(self.rect.centerx-player.rect.centerx) + abs(self.rect.centery-player.rect.centery)
        if distance<=self.trigger_distance:
            surface.blit(self.surface,camera.apply(self.rect))

world_data=[
[12,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,12],
[12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12],
[12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,10,0,0,0,0,12],
[12,0,0,0,0,0,3,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,5,0,0,0,0,12],
[12,0,14,0,0,0,109,0,0,0,0,0,0,0,0,0,0,0,0,0,110,0,0,0,0,0,0,0,0,0,0,12],
[12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,111,0,0,0,0,12],
[12,0,0,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12],
[12,0,0,0,0,0,13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12],
[12,0,0,0,0,0,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12],
[12,0,0,0,0,0,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12],
[12,0,0,0,0,0,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12],
[12,0,0,0,0,0,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12],
[12,0,0,0,0,0,11,0,0,0,0,0,13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12],
[12,0,0,0,0,0,0,0,0,0,0,0,12,0,108,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12],
[12,0,0,0,0,0,0,0,0,0,0,0,12,0,0,0,0,0,0,0,107,0,0,0,0,0,0,0,0,0,0,12],
[12,0,0,0,0,0,0,0,0,0,0,0,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12],
[12,0,0,0,0,0,0,0,0,0,0,0,11,0,0,0,3,4,4,4,5,0,0,0,0,0,0,0,0,0,0,12],
[12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,4,4,4,5,0,0,12],
[12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,0,0,0,0,12],
[12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,103,0,0,0,0,0,0,0,0,0,106,12],
[12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,104,0,0,0,0,0,0,0,0,0,7,12],
[12,0,0,0,100,0,0,0,0,101,0,0,0,0,0,102,0,0,1,2,0,0,0,0,105,0,0,0,0,1,1,2],
[12,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,1,1,1,2,2,2],
[2,1,1,1,1,1,1,1,2,2,2,1,1,1,1,1,1,1,2,2,6,6,6,6,6,6,2,2,2,2,2,2],
]

trap_group=pygame.sprite.Group()
mushroom_group=pygame.sprite.Group()
cannon_group=pygame.sprite.Group()
trap_down_group=pygame.sprite.Group()
#button_group=pygame.sprite.Group()
player=Player(100,700)
camera=Camera(screen_width,screen_height)
trap_group=pygame.sprite.Group()
mushroom_group=pygame.sprite.Group()
tutorial_world=World(world_data)
endlessworld=endlessworld(tile_size)
restart_button=button(screen_width//2-150,screen_height//1.25,restart_img,restart_hover_img)
main_menu_button=button(screen_width//2+150,screen_height//1.25,main_menu_img,menu_hover_img)
play_button=button(screen_width//2,screen_height//2-100,play_button,play_hover)
how_to_play_button=button(screen_width//2,screen_height//2,how_to_play_button,how_to_play_hover)
high_score_button=button(screen_width//2,screen_height//2+100,high_score_button,high_score_hover)
quit_button=button(screen_width//2,screen_height//2+200,quit_button,quit_hover)
continue_button=button(screen_width//2,screen_height//2,continue_button,continue_hover)
pause_restart_button=button(screen_width//2,screen_height//2+100,restart_img,restart_hover_img)
pause_menu_button=button(screen_width//2,screen_height//2+200,main_menu_img,menu_hover_img)
chaser_monster=monster(x=endlessworld.room_width-400,screen_height=screen_height,monster_width=800,num_frame=40,speed=1.5)

run=True
while run:
    clock.tick(fps)

    screen.blit(bg_img,(0,0))

    #draw_grid()
    if in_tutorial:
        #game_over=player.update(tutorial_world,game_over)

        screen.blit(menu_bg,(0,0))
        player.update(tutorial_world,game_over)
        camera.update(player.rect,shake_enable=False)
        cannon_group.update(bullet_group)
        tutorial_world.coin_group.update(player)
        trap_down_group.update(tutorial_world)
        for mushroom in mushroom_group:
            mushroom.update(player)
        for bullet in bullet_group:
            bullet.update(tutorial_world,player)
        tutorial_world.draw(screen,camera)
        for trap in trap_group:
            screen.blit(trap.image,camera.apply(trap.rect))
        for trap_down in trap_down_group:
            screen.blit(trap_down.image,camera.apply(trap_down.rect))
        for mushroom in mushroom_group:
            screen.blit(mushroom.image,camera.apply(mushroom.rect))
        for bullet in bullet_group:
            screen.blit(bullet.image,camera.apply(bullet.rect))
        for cannon in cannon_group:
            screen.blit(cannon.image,camera.apply(cannon.rect))
        player.draw(screen,camera)


    elif main_menu==True:
        screen.blit(menu_bg,(0,0))
        play_bgm('sound/menu_sound.flac',volume=0.5)
        if play_button.draw()==True:
            player.reset(100,700)
            chaser_monster.rect.x=player.rect.x-1000
            chaser_monster.rect.y=0
            endlessworld.reset_world()
            score=0
            game_over=0
            main_menu=False
        if how_to_play_button.draw()==True:
            game_over=0
            in_tutorial=True
            main_menu=False
            tutorial_world.reset()
            player.reset(100,700)
            player.vel_y=0
            player.dx=0
            player.dy=0
        high_score_button.draw()
        if quit_button.draw()==True:
            run=False
    else:
        screen.blit(bg_img,(0,0))
        if not paused and game_over==0:
            play_bgm('sound/bg_sound.mp3',volume=0.5)
            game_over = player.update(endlessworld, game_over)
            if game_over==0:
                if chaser_monster.update(player)==-1:
                    game_over=-1
            for coin in endlessworld.coin_group:
                if coin.update(player):
                    score+=1
            endlessworld.update(player,camera,chaser_monster)
            cannon_group.update(bullet_group)
            for trap_down in endlessworld.trap_down_group:
                trap_down.update(endlessworld)
            for mushroom in mushroom_group:
                mushroom.update(player)
            for bullet in bullet_group:
                result=bullet.update(endlessworld,player)
                if result==-1:
                    game_over=-1
            camera.update(player.rect,shake_enable=True)
        endlessworld.draw(screen,camera)
        for trap in trap_group:
            screen.blit(trap.image,camera.apply(trap.rect))
        for trap_down in endlessworld.trap_down_group:
            screen.blit(trap_down.image,camera.apply(trap_down.rect))
        for mushroom in mushroom_group:
            screen.blit(mushroom.image,camera.apply(mushroom.rect))
        player.draw(screen,camera)
        for cannon in cannon_group:
            screen.blit(cannon.image,camera.apply(cannon.rect))
        for bullet in bullet_group:
            screen.blit(bullet.image,camera.apply(bullet.rect))
        for coin in endlessworld.coin_group:
            screen.blit(coin.image,camera.apply(coin.rect))

        player.draw(screen,camera)
        chaser_monster.draw(screen,camera)
        draw_score(screen,score)

        if game_over == -1:
            if score>high_score:
                high_score=int(score)
            play_bgm('sound/dead_sound.mp3',volume=0.5)
            action=draw_game_over_screen()
            if action == "restart":
                player.reset(100,700)
                chaser_monster.rect.x = player.rect.x - 1000
                chaser_monster.rect.y = 0
                chaser_monster.speed=chaser_monster.base_speed
                bullet_group.empty()
                trap_down_group.empty()
                endlessworld.reset_world()
                score=0
                game_over=0
            elif action == "main":
                player.reset(100,700)
                chaser_monster.speed = chaser_monster.base_speed
                pygame.mixer.music.stop()
                bullet_group.empty()
                trap_down_group.empty()
                endlessworld.reset_world()
                score=0
                main_menu=True
        elif paused:
            #screen.blit(player.image,player.rect)
            pygame.mixer.music.pause()
            action=draw_pause_screen()
            if action == "continue":
                paused=False
                pygame.mixer.music.unpause()
            elif action == "pause_restart":
                player.reset(100,700)
                chaser_monster.rect.x = player.rect.x - 1000
                chaser_monster.rect.y = 0
                chaser_monster.speed = chaser_monster.base_speed
                bullet_group.empty()
                trap_down_group.empty()
                endlessworld.reset_world()
                score=0
                pygame.mixer.music.unpause()
                paused=False
            elif action == "pause_main":
                player.reset(100,700)
                main_menu=True
                chaser_monster.speed = chaser_monster.base_speed
                endlessworld.reset_world()
                score=0
                paused=False
                pygame.mixer.music.stop()
                '''quit_button.clicked=True'''

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if in_tutorial:
                    in_tutorial=False
                    main_menu=True
                elif not main_menu and game_over==0:
                    paused= True

    pygame.display.update()

pygame.quit()