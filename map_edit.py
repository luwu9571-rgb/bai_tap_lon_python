import pygame
import sys
import os

from script import mushroom

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAPS_PATH = os.path.join(BASE_DIR, "maps.py")

if os.path.exists(MAPS_PATH):
    from maps import map_list
else:
    map_list = [
        [[0 for _ in range(32)] for _ in range(24)]
    ]
pygame.init()
tile_size = 32
cols = 32
rows = 24
game_width=cols*tile_size
game_height=rows*tile_size
panel_height=90
screen=pygame.display.set_mode((game_width,game_height+panel_height))
pygame.display.set_caption("Endless world map editer (1024x768)")
clock=pygame.time.Clock()

current_map_index=0
current_tile=1
avalible_tile=[1,2,3,4,5,6,15,7,8,9,10,11,12,13,14]
tile_name={
1: "Grass", 2: "Dirt", 3: "Row Left", 4: "Row Mid", 5: "Row Right",
    6: "Trap",15:"Trap_down", 7: "Mushroom", 8: "Cannon L", 9: "Cannon R",10: "Coin",
    11: "Col Bot", 12: "Col Mid", 13: "Col Top", 14: "Single"
}

def get_frame(sheet_path,num_frames=1,index=0):
    sheet=pygame.image.load(sheet_path).convert_alpha()
    frame_width = sheet.get_width() // num_frames
    frame_height = sheet.get_height()
    return sheet.subsurface((index * frame_width, 0, frame_width, frame_height))


class mapeditor:
    def __init__(self,data,tile_size):
        self.tile_size=tile_size
        self.tile_list=[]
        self.tile_image={}

        cannon_img=get_frame("image/cannon.png",num_frames=8,index=0)
        self.tile_image[9]=pygame.transform.scale(cannon_img,(self.tile_size,self.tile_size))
        self.tile_image[8]=pygame.transform.flip(self.tile_image[9],True,False)
        mushroom_img=get_frame("image/shroom.png",num_frames=4,index=0)
        self.tile_image[7]=pygame.transform.scale(mushroom_img,(self.tile_size,self.tile_size))
        coin_img=get_frame("image/Coin.png",num_frames=4,index=0)
        self.tile_image[10]=pygame.transform.scale(coin_img,(self.tile_size,self.tile_size))

        image_files = {
            1: "image/grass.png", 2: "image/dirt.png", 3: "image/platform_row_left.png",
            4: "image/platform_row_mid.png", 5: "image/platform_row_right.png",
            6: "image/trap.png",15:"image/trap_down.png", 11: "image/platform_col_bot.png",
            12: "image/platform_col_mid.png", 13: "image/platform_col_top.png",
            14: "image/platform_single.png"
        }

        for t_id, file_name in image_files.items():
            img=pygame.image.load(file_name).convert_alpha()
            self.tile_image[t_id]=pygame.transform.scale(img,(self.tile_size,self.tile_size))
        self.load_data(data)

    def load_data(self,data):
        self.tile_list.clear()
        for r,row in enumerate(data):
            for c,tile in enumerate(row):
                if tile in self.tile_image:
                    x=c*self.tile_size
                    y=r*self.tile_size
                    img=self.tile_image[tile]
                    img_rect=img.get_rect(topleft=(x,y))
                    self.tile_list.append((img,img_rect))
    def draw(self,surface):
        for img,rect in self.tile_list:
            surface.blit(img,rect)


def save_all_maps_to_file(filename="maps.py"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("map_list = [\n")
        for m in map_list:
            f.write("    [\n")
            for row in m[:rows]:
                f.write("        " + str(row[:cols]) + ",\n")
            f.write("    ],\n")
        f.write("]\n")
    print("Đã lưu map thành công!")

editor_world=mapeditor(map_list[current_map_index],tile_size)
running=True
while running:
    clock.tick(60)
    need_reload_data=False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        elif event.type == pygame.MOUSEWHEEL:
            idx = avalible_tile.index(current_tile) if current_tile in avalible_tile else 0
            if event.y>0:
                current_tile =avalible_tile[(idx + 1) % len(avalible_tile)]
            elif event.y<0:
                current_tile =avalible_tile[(idx - 1) % len(avalible_tile)]
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_all_maps_to_file()
            elif event.key == pygame.K_RIGHT:
                if current_map_index<len(map_list) - 1:
                    current_map_index+=1
                    need_reload_data=True
            elif event.key == pygame.K_LEFT:
                if current_map_index > 0:
                    current_map_index-=1
                    need_reload_data=True
            elif event.key == pygame.K_n:
                map_list.append([[0 for _ in range(cols)] for _ in range(rows)])
                current_map_index=len(map_list)-1
                need_reload_data=True
    mouse_button=pygame.mouse.get_pressed()
    mx,my=pygame.mouse.get_pos()

    if my<game_height:
        gx,gy=mx//tile_size,my//tile_size
        if 0 <= gx < cols and 0<=gy<rows:
            if mouse_button[0]:
                if map_list[current_map_index][gy][gx] != current_tile:
                    map_list[current_map_index][gy][gx]=current_tile
                    need_reload_data=True
            elif mouse_button[2]:
                if map_list[current_map_index][gy][gx] != 0:
                    map_list[current_map_index][gy][gx]=0
                    need_reload_data=True
    elif my>= game_height+35:
        if mouse_button[0]:
            p_idx = (mx - 10 ) // (tile_size+12)
            if 0 <= p_idx < len(avalible_tile):
                current_tile=avalible_tile[p_idx]
    if need_reload_data:
        editor_world.load_data(map_list[current_map_index])
    screen.fill((30,30,30))
    editor_world.draw(screen)
    for r in range(rows):
        for c in range(cols):
            pygame.draw.rect(screen,(60,60,60),(c*tile_size,r*tile_size,tile_size,tile_size),1)
    pygame.draw.rect(screen,(20,20,20),(0,game_height,game_width,panel_height))
    for i, t_id in enumerate(avalible_tile):
        px=10+i*(tile_size+12)
        py=game_height+35
        prect=(px,py,tile_size,tile_size)
        if t_id in editor_world.tile_image:
            screen.blit(editor_world.tile_image[t_id],prect)
        if t_id == current_tile:
            pygame.draw.rect(screen,(255,255,0),prect,3)
        else:
            pygame.draw.rect(screen,(100,100,100),prect,1)
        #screen.blit(editor_world.tile_image[t_id],prect)

    pygame.display.flip()
pygame.quit()
sys.exit()