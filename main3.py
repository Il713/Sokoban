import pygame
from level_extraction import extract
import os
from copy import deepcopy
fps=20

tile=(50,50)

class Game:
    def __init__(self):
        self.tile=(20,20)
        self.run=True
        self.level=None
        self.win=pygame.display.set_mode((1000,800))
        self.size=None
        self.i=0
        self.count=0
        self.dir='front'
        sprite='sprite'
        self.char={}
        self.char2={}
        for x in os.listdir(sprite):
            if x not in self.char:
                self.char[x]=[]
                self.char2[x]=[]
            for y in os.listdir(sprite+'/'+x):
                self.char[x]+=[pygame.image.load(sprite+'/'+x+'/'+y)]
                self.char2[x]+=[pygame.image.load(sprite+'/'+x+'/'+y)]
        self.sprites={'#':pygame.image.load('wall.png'),'$':pygame.image.load('box.png'),'@':self.char,'.':pygame.Surface((20,20)),
                      '*':pygame.image.load('box.png'),'+':self.char2}
        self.sprites['*'].set_alpha(50)
        self.sprites['.'].fill((250,100,100))
        for x in self.sprites:
            if x == '@':
                for y in self.sprites[x]:
                    for z in y:
                        for i in range(len(self.sprites[x][y])):
                            self.sprites[x][y][i]=pygame.transform.smoothscale(self.sprites[x][y][i],tile)
            elif x == '+':
                for y in self.sprites[x]:
                    for z in y:
                        for i in range(len(self.sprites[x][y])):
                            self.sprites[x][y][i]=pygame.transform.smoothscale(self.sprites[x][y][i],tile)
                            s=pygame.Surface(tile)
                            s.fill((250,100,100))
                            s.blit(self.sprites[x][y][i],(0,0))
                            self.sprites[x][y][i]=s

            else:
                self.sprites[x]=pygame.transform.smoothscale(self.sprites[x],tile)
        self.clock=pygame.time.Clock()
        self.x,self.y=None,None
        self.restart=False
        
    def refresh(self):
        self.win.fill((0,0,0))
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                elmt=self.level[i][j]
                if elmt!=' ':
                    if elmt in ['@','+']:
                        self.win.blit(self.sprites[elmt][self.dir][self.i],(j*tile[0],i*tile[1]))
                    else:
                        self.win.blit(self.sprites[elmt],(j*tile[0],i*tile[1]))
        pygame.display.flip()
                
                    

    def loop(self):
        self.lv_name=1
        self.run=True
        if self.lv_name:
            self.level,self.x,self.y=extract('soko2.txt')
            n=0
            for x in self.level:
                if n<len(x):
                    n=len(x)
            for l in self.level:
                for _ in range(n-len(l)):
                    l+=[' ']
            self.size=len(self.level),n
        while self.run:
            
            self.count+=1
            if self.count>50:
                self.count=0
                self.i+=1
                self.i=self.i%2
        
            self.clock.tick()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_LEFT:
                        self.dir='left'
                        if self.level[self.y][self.x-1] in [' ','$','.','*']:
                            if self.x>0 and self.level[self.y][self.x-1]=='$':
                                if self.level[self.y][self.x-2]==' ':
                                    self.level[self.y][self.x-2]='$'
                                    self.level[self.y][self.x-1]=' '
                                elif self.level[self.y][self.x-2]=='.':
                                    self.level[self.y][self.x-2]='*'
                                    self.level[self.y][self.x-1]=' '
                            elif self.x>0 and self.level[self.y][self.x-1]=='*':
                                if self.level[self.y][self.x-2]==' ':
                                    self.level[self.y][self.x-2]='$'
                                    self.level[self.y][self.x-1]='.'
                                elif self.level[self.y][self.x-2]=='.':
                                    self.level[self.y][self.x-2]='*'
                                    self.level[self.y][self.x-1]='.'
                            else:
                                if self.level[self.y][self.x-1]==' ':
                                    if self.level[self.y][self.x]=='@':
                                        self.level[self.y][self.x-1]='@'
                                        self.level[self.y][self.x]=' '
                                    else:
                                        self.level[self.y][self.x-1]='@'
                                        self.level[self.y][self.x]='.'
                                elif self.level[self.y][self.x-1]=='.':
                                    if self.level[self.y][self.x]=='+':
                                        self.level[self.y][self.x-1]='+'
                                        self.level[self.y][self.x]='.'
                                    else:
                                        self.level[self.y][self.x-1]='+'
                                        self.level[self.y][self.x]=' '
                                self.x-=1
                    if event.key==pygame.K_RIGHT:
                        self.dir='right'
                        if self.x<n-1 and self.level[self.y][self.x+1] in [' ','$','.','*']:
                            if self.level[self.y][self.x+1]=='$':
                                if self.level[self.y][self.x+2]==' ':
                                    self.level[self.y][self.x+2]='$'
                                    self.level[self.y][self.x+1]=' '
                                elif self.level[self.y][self.x+2]=='.':
                                    self.level[self.y][self.x+2]='*'
                                    self.level[self.y][self.x+1]=' '
                            elif self.level[self.y][self.x+1]=='*':
                                if self.level[self.y][self.x+2]==' ':
                                    self.level[self.y][self.x+2]='$'
                                    self.level[self.y][self.x+1]='.'
                                elif self.level[self.y][self.x+2]=='.':
                                    self.level[self.y][self.x+2]='*'
                                    self.level[self.y][self.x+1]='.'
                            else:
                                if self.level[self.y][self.x+1]==' ':
                                    if self.level[self.y][self.x]=='@':
                                        self.level[self.y][self.x+1]='@'
                                        self.level[self.y][self.x]=' '
                                    else:
                                        self.level[self.y][self.x+1]='@'
                                        self.level[self.y][self.x]='.'
                                else:
                                    if self.level[self.y][self.x]=='@':
                                        self.level[self.y][self.x+1]='+'
                                        self.level[self.y][self.x]=' '
                                    else:
                                        self.level[self.y][self.x+1]='+'
                                        self.level[self.y][self.x]='.'
                                self.x+=1
                    if event.key==pygame.K_UP:
                        self.dir='back'
                        if self.y>0 and self.level[self.y-1][self.x] in [' ','$','.','*']:
                            if self.level[self.y-1][self.x]=='$':
                                if self.level[self.y-2][self.x]==' ':
                                    self.level[self.y-2][self.x]='$'
                                    self.level[self.y-1][self.x]=' '
                                elif self.level[self.y-2][self.x]=='.':
                                    self.level[self.y-2][self.x]='*'
                                    self.level[self.y-1][self.x]=' '
                            elif self.level[self.y-1][self.x]=='*':
                                if self.level[self.y-2][self.x]==' ':
                                    self.level[self.y-2][self.x]='$'
                                    self.level[self.y-1][self.x]='.'
                                elif self.level[self.y-2][self.x]=='.':
                                    self.level[self.y-2][self.x]='*'
                                    self.level[self.y-1][self.x]='.'
                            else:
                                if self.level[self.y-1][self.x]==' ':
                                    if self.level[self.y][self.x]=='@':
                                        self.level[self.y-1][self.x]='@'
                                        self.level[self.y][self.x]=' '
                                    else:
                                        self.level[self.y-1][self.x]='@'
                                        self.level[self.y][self.x]='.'
                                else:
                                    if self.level[self.y][self.x]=='@':
                                        self.level[self.y-1][self.x]='+'
                                        self.level[self.y][self.x]=' '
                                    else:
                                        self.level[self.y-1][self.x]='+'
                                        self.level[self.y][self.x]='.'
                                self.y-=1
                    if event.key==pygame.K_DOWN:
                        self.dir='front'
                        if self.y<len(self.level)-1 and self.level[self.y+1][self.x] in [' ','$','.','*']:
                            if self.level[self.y+1][self.x]=='$':
                                if self.level[self.y+2][self.x]==' ':
                                    self.level[self.y+2][self.x]='$'
                                    self.level[self.y+1][self.x]=' '
                                elif self.level[self.y+2][self.x]=='.':
                                    self.level[self.y+2][self.x]='*'
                                    self.level[self.y+1][self.x]=' '
                            elif self.level[self.y+1][self.x]=='*':
                                if self.level[self.y+2][self.x]==' ':
                                    self.level[self.y+2][self.x]='$'
                                    self.level[self.y+1][self.x]='.'
                                elif self.level[self.y+2][self.x]=='.':
                                    self.level[self.y+2][self.x]='*'
                                    self.level[self.y+1][self.x]='.'
                            else:
                                if self.level[self.y+1][self.x]==' ':
                                    if self.level[self.y][self.x]=='@':
                                        self.level[self.y+1][self.x]='@'
                                        self.level[self.y][self.x]=' '
                                    else:
                                        self.level[self.y+1][self.x]='@'
                                        self.level[self.y][self.x]='.'
                                else:
                                    if self.level[self.y][self.x]=='@':
                                        self.level[self.y+1][self.x]='+'
                                        self.level[self.y][self.x]=' '
                                    else:
                                        self.level[self.y+1][self.x]='+'
                                        self.level[self.y][self.x]='.'
                                self.y+=1
                    if event.key==pygame.K_ESCAPE:
                        self.run=False
                    if event.key==pygame.K_SPACE:
                        self.restart=True
            if self.restart:
                self.run=False
            self.refresh()
        if self.restart:
            self.__init__()
            self.loop()

PV=Game()
PV.loop()
pygame.quit()

