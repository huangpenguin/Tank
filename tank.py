import pygame, time, random, sys
from random import randint
from pygame.sprite import collide_rect
COLOR_BLACK = pygame.Color(0, 0, 0)
COLOR_RED = pygame.Color(255, 0, 0)
#######some code comes from Java version(https://blog.csdn.net/O_C_E_A_N_/article/details/123974373)
####################################################################################################

class MainGame():
    window = None  # 游戏主窗口
    SCREEN_WIDTH = 1300
    SCREEN_HEIGHT = 700
    TANK_P1 = None
    FLAG = None
    EnemyTank_list = []  # 敌方坦克列表
    EnemyTank_count = 5  # 创建的坦克数量
    Bullet_list = []  # 存储我方子弹的列表
    Enemy_bullet_list = []  # 存储敌方坦克
    Num_Key = 0
    Explode_list = []
    Wall_count = 20
    Wall_list = []  # 墙壁列表
    defeatNum = 5
    remainLive = 3

    def __init__(self):
        pass

    def startGame(self):  # 开始游戏
        pygame.display.init()
        MainGame.window = pygame.display.set_mode([MainGame.SCREEN_WIDTH, MainGame.SCREEN_HEIGHT])  # 加载游戏窗口（看文档）
        self.createMyTank()  # 创建我方坦克
        self.createFlag()
        start = Music('img/start.wav')
        start.play()
        pygame.display.set_caption('Battle City')  # 设置标题
        self.createEnemyTank(MainGame.EnemyTank_count)
        self.createWalls(MainGame.Wall_count)  # 调用展示墙壁的方法

        while True:  # 让窗口持续刷新
            MainGame.window.fill(COLOR_BLACK)  # 填充为黑色
            self.getEvent()
            self.displayWalls()
            MainGame.window.blit(self.getTextSurface('还需要击败敌人%d' % MainGame.defeatNum), (5, 5))  # 将绘制文字的小画布粘贴到窗口中
            MainGame.window.blit(self.getTextSurface('剩余命数%d' % MainGame.remainLive), (5, 23))  # 将绘制文字的小画布粘贴到窗口中
            if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                MainGame.TANK_P1.displayTank()  # 将我方坦克加入窗口
            else:
                del MainGame.TANK_P1  # 我方坦克被击中则删去该对象
                MainGame.TANK_P1 = None
            if MainGame.FLAG and MainGame.FLAG.live:
                MainGame.FLAG.dispalyFlag()  # 将旗帜加入窗口
            self.displayEnemyTank()  # 将敌方坦克加入窗口
            if MainGame.TANK_P1 and not MainGame.TANK_P1.stop:  # 坦克存在并且打开开关时允许移动
                MainGame.TANK_P1.move()
                MainGame.TANK_P1.hitWalls()
                MainGame.TANK_P1.hitEnemyTank()
            if len(self.EnemyTank_list) < 5:
                self.createEnemyTank(MainGame.EnemyTank_count - len(self.EnemyTank_list))#刷新敌方坦克
            if len(self.Wall_list) < 20:
                self.createWalls(MainGame.Wall_count - len(self.Wall_list))
            self.displayBullet()  # 调用渲染子弹列表的方法
            self.displayEnemyBullet()  # 敌方坦克的子弹
            self.displayExplodes()
            time.sleep(0.01)  # 调整游戏速度
            pygame.display.update()
            if MainGame.defeatNum == 0 or MainGame.remainLive == 0 or not MainGame.FLAG.live:
                break

        while True:
            self.blitEndWord()
            pygame.display.update()
            pygame.time.wait(1000)
            self.endGame()

    def createMyTank(self):
        MainGame.TANK_P1 = MyTank(400, 600)  # 创建我方坦克
        music = Music('img/add.wav')
        music.play()

    def createEnemyTank(self, count):  # 创建敌方坦克
        top = 100
        for i in range(count):
            rand = random.randint(1, 3)
            if rand == 1:
                left = 100
            elif rand == 2:
                left = 650
            elif rand == 3:
                left = 1200
            speed = random.randint(3, 4)
            eTtank = EnemyTank(left, top, speed)
            MainGame.EnemyTank_list.append(eTtank)

    def createWalls(self,count):  # 创建墙壁的方法
        if len(self.Wall_list)<=2:
            wall2 = Wall(0, 0)
            L_left = MainGame.SCREEN_WIDTH / 2 - MainGame.FLAG.rect.width - wall2.rect.width
            L_top = MainGame.SCREEN_HEIGHT - wall2.rect.height
            for i in range(0, 4):
                wall = Wall(L_left + wall2.rect.width * i, L_top - wall2.rect.height)
                MainGame.Wall_list.append(wall)
            wall = Wall(L_left + wall2.rect.width * 3, L_top)
            MainGame.Wall_list.append(wall)
            wall = Wall(L_left + wall2.rect.width * 0, L_top)
            MainGame.Wall_list.append(wall)
        for i in range(count):
            sameflag = 0
            wall = Wall(randint(0, 1300)//65*65, randint(0, 700)//35*35)
            if MainGame.TANK_P1 and collide_rect(MainGame.TANK_P1, wall):
                sameflag=1
            if sameflag:
                continue
            for tank in MainGame.EnemyTank_list:
                if collide_rect(tank, wall):
                    sameflag=1
                    break
            if sameflag:
                continue
            for wall0 in MainGame.Wall_list:
                if collide_rect(wall0, wall):
                    sameflag=1
                    break
            if sameflag:
                continue
            MainGame.Wall_list.append(wall)





    def displayEnemyTank(self):  # 将坦克加入到窗口中
        for eTank in MainGame.EnemyTank_list:
            if eTank.live:
                eTank.displayTank()
                eTank.randMove()  # 坦克移动
                eTank.hitWalls()  # 调用敌方坦克与墙壁的碰撞方法
                eBullet = eTank.shot()  # 敌方坦克射击,因为继承关系，所以有shot函数
                eTank.hitMyTank()
                if eBullet:
                    MainGame.Enemy_bullet_list.append(eBullet)  # 将敌方子弹坦克加入列表
            else:
                MainGame.EnemyTank_list.remove(eTank)

    def displayBullet(self):  # 将我方子弹加入窗口
        for bullet in MainGame.Bullet_list:
            if bullet.live:  # 如果子弹还存在，则展示，否则，移除子弹
                bullet.displayBullet()
                bullet.bulletMove()
                bullet.hitEnemyTank()  # 调用我方子弹和敌方坦克的碰撞方法
                bullet.hitWalls()  # 判断子弹撞墙
                bullet.hitFlag()
            else:
                MainGame.Bullet_list.remove(bullet)

    def displayExplodes(self):  # 新增方法，展示爆炸效果列表
        for explode in MainGame.Explode_list:
            if explode.live:
                explode.displayExplode()
            else:
                MainGame.Explode_list.remove(explode)

    def displayEnemyBullet(self):  # 将敌方子弹加入窗口
        for ebullet in MainGame.Enemy_bullet_list:
            if ebullet.live:  # 如果子弹还存在，则展示，否则，移除子弹
                ebullet.displayBullet()
                ebullet.bulletMove()  # 让子弹移动
                ebullet.hitWalls()
                ebullet.hitFlag()
                if MainGame.TANK_P1 and MainGame.TANK_P1.live:  # 坦克存在并活着才能调用
                    ebullet.hitMyTank()
            else:
                MainGame.Enemy_bullet_list.remove(ebullet)

    def getTextSurface(self, text):
        pygame.font.init()  # 初始化字体模块
        font = pygame.font.SysFont('kaiti', 18)  # 选中一个字体
        textSurface = font.render(text, True, COLOR_RED)  # 进行绘制
        return textSurface

    def getEvent(self):  # 获取事件，比如鼠标事件、键盘事件
        eventList = pygame.event.get()  # 获取
        for event in eventList:
            if event.type == pygame.QUIT:  # 判断是否点击退出
                self.endGame()
            if event.type == pygame.KEYDOWN:  # 判断按键按下，并判断是哪个键
                if event.key == pygame.K_ESCAPE and not MainGame.TANK_P1:  # ESC按键重生
                    self.createMyTank()
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    MainGame.Num_Key += 1
                if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                    if event.key == pygame.K_LEFT:  # 左方向键
                        print('左')
                        MainGame.TANK_P1.direction = 'L'  # 改变坦克的方向
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_RIGHT:
                        print('右')
                        MainGame.TANK_P1.direction = 'R'  # 改变坦克的方向
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_UP:
                        print('上')
                        MainGame.TANK_P1.direction = 'U'  # 改变坦克的方向
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_DOWN:
                        print('下')
                        MainGame.TANK_P1.direction = 'D'  # 改变坦克的方向
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_SPACE:
                        if len(MainGame.Bullet_list) < 5:
                            m = Bullet(MainGame.TANK_P1)  # 产生一个子弹
                            MainGame.Bullet_list.append(m)
                            print('射击')
                            music = Music('img/fire.wav')
                            music.play()

            if event.type == pygame.KEYUP:  # 将坦克的移动状态修改
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    MainGame.Num_Key -= 1
                if ((
                        event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN) and MainGame.Num_Key == 0):
                    if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                        MainGame.TANK_P1.stop = True

    def displayWalls(self):
        for wall in MainGame.Wall_list:
            if wall.live:
                wall.dispalyWall()
            else:
                MainGame.Wall_list.remove(wall)

    def endGame(self):  # 结束游戏
        print('Game over')
        pygame.quit()
        sys.exit(0)
        # exit(0)  # 结束Python解释器

    def blitEndWord(self):
        image = EndWord()
        image.dispalyEndWord()

    def createFlag(self):
        MainGame.FLAG = Flag()

    def restart(self):
        self.startGame()


class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #for collision derivation


class Tank(BaseItem):
    def __init__(self, left, top):
        self.images = {'U': pygame.image.load('img/p1tankU.gif'),
                       'D': pygame.image.load('img/p1tankD.gif'),
                       'L': pygame.image.load('img/p1tankL.gif'),
                       'R': pygame.image.load('img/p1tankR.gif')
                       }
        self.direction = 'U'
        self.image = self.images[self.direction]  # 根据坦克的方向选择照片
        self.rect = self.image.get_rect()  # 坦克所在的区域
        self.rect.left = left
        self.rect.top = top  # 指定坦克的初始化位置，分别距离x，y轴的距离
        self.speed = 5
        self.stop = True
        self.live = True
        self.oldLeft = self.rect.left  # 新增属性，记录坦克之前的坐标
        self.oldTop = self.rect.top

    def move(self):  # 坦克移动
        self.oldLeft = self.rect.left  # 新增属性，记录坦克之前的坐标
        self.oldTop = self.rect.top  # 记录之前的坐标
        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'R':
            if self.rect.left + self.rect.height < MainGame.SCREEN_WIDTH:
                self.rect.left += self.speed
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < MainGame.SCREEN_HEIGHT:
                self.rect.top += self.speed

    def stay(self):
        self.rect.left = self.oldLeft
        self.rect.top = self.oldTop

    def hitWalls(self):  # 新增坦克和墙壁碰撞方法
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(wall, self):
                self.stay()

    def shot(self):  # 坦克射击
        return Bullet(self)

    def displayTank(self):  # 坦克进行显示（将坦克这个Surface绘制到窗口中，用blit()）
        self.image = self.images[self.direction]  # 重置坦克的图像
        MainGame.window.blit(self.image, self.rect)  # 将坦克加入到窗口中


class MyTank(Tank):
    def __init__(self, left, top):
        super(MyTank, self).__init__(left, top)

    def hitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if pygame.sprite.collide_rect(eTank, self):
                self.stay()


class EnemyTank(Tank):
    def __init__(self, left, top, speed):
        super(EnemyTank, self).__init__(left, top)
        self.images = {'U': pygame.image.load('img/enemy1U.gif'),
                       'D': pygame.image.load('img/enemy1D.gif'),
                       'L': pygame.image.load('img/enemy1L.gif'),
                       'R': pygame.image.load('img/enemy1R.gif')
                       }
        self.direction = self.randDirection()
        self.image = self.images[self.direction]  # 根据坦克的方向选择照片
        self.rect = self.image.get_rect()  # 坦克所在的区域
        self.rect.left = left
        self.rect.top = top  # 指定坦克的初始化位置，分别距离x，y轴的距离
        self.speed = speed
        self.stop = True
        self.step = random.randint(38, 53)  # 新增步数属性，用来控制敌方坦克随机移动

    def randDirection(self):  # 用来随机生成坦克的方向
        num = random.randint(1, 4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        elif num == 4:
            return 'R'

    def randMove(self):
        if self.step <= 0:
            self.direction = self.randDirection()  # 一定距离后改变方向
            self.step = random.randint(23, 43)  # 重置步数
        else:
            self.move()
            self.step -= 1

    def shot(self):
        num = random.randint(1, 70)
        if num == 1:
            return Bullet(self)

    def hitMyTank(self):
        if MainGame.TANK_P1 and MainGame.TANK_P1.live:
            if pygame.sprite.collide_rect(self, MainGame.TANK_P1):
                self.stay()


class Bullet(BaseItem):
    def __init__(self, tank):
        self.image = pygame.image.load('img/enemymissile.gif')  # 图像
        self.direction = tank.direction  # 方向
        self.rect = self.image.get_rect()
        self.speed = 7  # 速度
        self.live = True  # 判断子弹是否应存在

        if self.direction == 'U':  # 起始位置
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top - self.rect.width / 2 + tank.rect.width / 2

    def bulletMove(self):  # 子弹移动
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.live = False
        elif self.direction == 'D':
            if self.rect.top < MainGame.SCREEN_HEIGHT - self.rect.height:
                self.rect.top += self.speed
            else:
                self.live = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.live = False
        elif self.direction == 'R':
            if self.rect.left < MainGame.SCREEN_WIDTH - self.rect.width:
                self.rect.left += self.speed
            else:
                self.live = False

    def displayBullet(self):  # 子弹显示
        MainGame.window.blit(self.image, self.rect)

    def hitEnemyTank(self):  # 新增我方子弹碰撞敌方坦克的方法
        for eTank in MainGame.EnemyTank_list:
            if pygame.sprite.collide_rect(eTank, self):
                self.live = False  # 子弹不再存回
                eTank.live = False  # 坦克不再存活
                explode = Explode(eTank)  # 产生一个爆炸效果
                MainGame.Explode_list.append(explode)  # 将爆炸效果加入到爆炸效果列表
                music = Music('img/hit.wav')
                music.play()
                MainGame.defeatNum -= 1

    def hitMyTank(self):  # 新增敌方子弹和我方坦克
        # 因为前面已经遍历了敌方子弹，所以这里只需要判断一个子弹
        if pygame.sprite.collide_rect(self, MainGame.TANK_P1):
            self.live = False  # 修改子弹状态
            MainGame.TANK_P1.live = False  # 修改我方坦克状态
            explode = Explode(MainGame.TANK_P1)  # 产生爆炸效
            MainGame.Explode_list.append(explode)
            music = Music('img/hit.wav')
            music.play()
            MainGame.remainLive -= 1

    def hitWalls(self):  # 子弹与墙壁碰撞
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(wall, self):
                self.live = False  # 修改属性
                wall.hp -= 1
            if wall.hp <= 0:
                wall.live = False

    def hitFlag(self):  # 子弹与旗帜碰撞
        if pygame.sprite.collide_rect(MainGame.FLAG, self):
            self.live = False  # 修改属性
            MainGame.FLAG.live = False


class Explode():
    def __init__(self, tank):
        self.rect = tank.rect
        self.step = 0
        self.images = [
            pygame.image.load('img/blast0.gif'),
            pygame.image.load('img/blast1.gif'),
            pygame.image.load('img/blast2.gif'),
            pygame.image.load('img/blast3.gif'),
            pygame.image.load('img/blast4.gif')]
        self.image = self.images[self.step]
        self.live = True  # 一开始要进行显示

    def displayExplode(self):  # 展示子弹
        if self.step < len(self.images):
            MainGame.window.blit(self.image, self.rect)
            self.image = self.images[self.step]
            self.step += 1
        else:
            self.step = 0
            self.live = False  # 不再进行显示


class Wall():
    count = 0
    def __init__(self, left, top):
        self.image = pygame.image.load('img/walls.gif')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.live = True  # 因为子弹打墙壁要是否消失，所以定义该属性
        self.hp = 3  # 墙壁生命值
        Wall.count += 1
    def dispalyWall(self):  # 展示墙壁
        MainGame.window.blit(self.image, self.rect)

class EndWord():
    def __init__(self):
        self.images = [pygame.image.load('img/over.gif'),
                       pygame.image.load('img/win.gif')]
        if MainGame.remainLive == 0:
            self.image = self.images[0]
        if MainGame.defeatNum == 0:
            self.image = self.images[1]
        if not MainGame.FLAG.live:
            self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.left = 650
        self.rect.top = 350

    def dispalyEndWord(self):  # 展示
        MainGame.window.blit(self.image, self.rect)


class Flag():
    def __init__(self):
        self.image = pygame.image.load('img/flag.gif')
        self.rect = self.image.get_rect()
        self.rect.left = MainGame.SCREEN_WIDTH / 2 - self.rect.width / 2
        self.rect.top = MainGame.SCREEN_HEIGHT - self.rect.height
        self.live = True

    def dispalyFlag(self):  # 展示
        MainGame.window.blit(self.image, self.rect)


class Music():
    def __init__(self, fileName):
        self.fileName = fileName
        pygame.mixer.init()
        pygame.mixer.music.load(self.fileName)

    def play(self):  # 开始播放音乐
        pygame.mixer.music.play()
