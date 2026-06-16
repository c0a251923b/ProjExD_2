import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1100, 650
DELTA={pg.K_UP:(0,-5),pg.K_DOWN:(0,+5),pg.K_LEFT:(-5,0),pg.K_RIGHT:(+5,0)}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


#画面外判定
def check_bound(rct:pg.Rect) -> tuple[bool,bool]:

    """
    引数:こうかとんRectまたは爆弾Rect
    戻り値：横方向判定、縦方向判定
    画面内ならTrue,画面外ならFalse
    """

    yoko,tate = True,True
    if rct.left<0 or WIDTH < rct.right:
        yoko = False
    if rct.top<0 or HEIGHT < rct.bottom:
        tate = False
    return yoko,tate

#演習1ゲームオーバー画面
def gameover(screen:pg.Surface) -> None:
    """
    引数:スクリーンSurface
    戻り値:None
    ゲームオーバーの画面作成
    """

    black_screen = pg.Surface((WIDTH,HEIGHT))#黒surface
    pg.draw.rect(black_screen,(0,0,0),(0,0,WIDTH,HEIGHT))
    black_screen.set_alpha(200)#透明度

    #Game Over 文字表示処理
    font = pg.font.Font(None,80)
    txt = font.render("Game Over",True,(255,255,255))
    black_screen.blit(txt,[400,300])
    #こうかとん（悲しい）画面表示
    kk_cry_img = pg.image.load("fig/8.png")
    black_screen.blit(kk_cry_img,[330,290])
    black_screen.blit(kk_cry_img,[730,290])

    screen.blit(black_screen,[0,0])
    pg.display.update()#画面再読み込み
    time.sleep(5)#5秒停止
    return

#演習2時間とともに爆弾が拡大、加速する
def init_bb_imgs() -> tuple[list[pg.Surface],list[int]]:
    """
    時間とともに爆弾が拡大，加速する関数
    引数:Surface
    返り値:爆弾の大きさ、速さ
    """





def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    #爆弾の初期化
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)  #半径10の赤円
    bb_img.set_colorkey((0,0,0))  
    
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0,WIDTH)
    bb_rct.centery = random.randint(0,HEIGHT)
    vx,vy = 5,5


    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        #爆弾と当たると終了    
        if kk_rct.colliderect(bb_rct):
            gameover(screen)  #ゲームオーバー画面表示
            return 
        screen.blit(bg_img, [0, 0]) 
        #こうかとん移動
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        #こうかとん画面外処理
        if check_bound(kk_rct) != (True,True):  #画面外なので動きをキャンセル
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)


        bb_rct.move_ip(vx,vy)
        #爆弾画面外処理
        yoko,tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1    

        screen.blit(bb_img,bb_rct)


        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
