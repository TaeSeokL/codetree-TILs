from collections import deque
from copy import deepcopy

def horse_move_and_fight(num,d):
    dy, dx = dir[d]
    moving_horse = deque()
    tmp = deque()
    tmp.append(num)
    demage_horse = []

    # 이동명령을 받은 말을 기준으로 이동방향에 뭐가 있는지 파악해서 다른 기사가 있다면
    # 큐에 추가해서 다음 탐색을 이어나감.
    for (y,x) in horse_index[num]:
        ny, nx = y+dy, x+dx

        if 0<=ny<l and 0<=nx<l:
            if board[ny][nx] == 2:
                return

            elif horse_board[ny][nx] != num and horse_board[ny][nx] != 0 :
                if horse_board[ny][nx] not in moving_horse:
                    moving_horse.append(horse_board[ny][nx])

    # 전에 단계에서 기사들을 추가했으면 이 기사들을 대상으로도 똑같은 것을 진행함.
    # 움직여야하는 모든 기사들을 tmp에 추가해줌.
    while moving_horse:
        horse_num = moving_horse.popleft()
        tmp.append(horse_num)
        demage_horse.append(horse_num)

        for (y,x) in horse_index[horse_num]:
            ny, nx = y + dy, x + dx

            if 0 <= ny < l and 0 <= nx < l:
                if board[ny][nx] == 2:
                    return

                elif horse_board[ny][nx] != horse_num and horse_board[ny][nx] != 0:
                    if horse_board[ny][nx] not in moving_horse:
                        moving_horse.append(horse_board[ny][nx])

    # 기사들을 이동시켜줌.
    while tmp:
        horse_num = tmp.popleft()
        temp = []
        for (y,x) in horse_index[horse_num]:
            ny, nx = y + dy, x + dx
            horse_board[y][x] = 0
            temp.append((ny,nx))

        horse_index[horse_num] = temp

    for i in range(1, len(horse_index)):
        for (y,x) in horse_index[i]:
            horse_board[y][x] = i


    # 함정 계산
    for i in range(len(demage_horse)):
        for y,x in bomb_index:
            if (y,x) in horse_index[demage_horse[i]] and horse_hp[demage_horse[i]] > 0:
                horse_hp[demage_horse[i]] -= 1




if __name__=='__main__':
    l,n,q = map(int,input().split())        # l = 맵크기, n = 기사수, q = 왕 명령 수

    board = [list(map(int,input().split())) for _ in range(l)]  # 함정과 벽, 빈칸 배열
    bomb_index = []                             # 함정 위치 인덱스 배열
    for i in range(l):
        for j in range(l):
            if board[i][j] == 1:
                bomb_index.append((i,j))


    horse_board = [[0]*l for _ in range(l)]     # 기사들 저장할 배열
    horse_index = [[] for _ in range(n+1)]      # 기사 위치 인덱스 배열
    horse_ori_hp = [0]
    dir = [(-1,0),(0,1),(1,0),(0,-1)]           # 이동방향

    # 기사 위치를 표시해줌
    for i in range(1,n+1):
        r,c,h,w,k = map(int,input().split())
        horse_ori_hp.append(k)
        # i = 기사 번호, 각 기사는 사각형태기 때문에
        # y,x 범위를 설정해서 기사의 크기만큼 기사번호를 할당해줌.
        # 기사 위치 관리 인덱스에도 추가해줌.
        for y in range(r-1,r+h-1):
            for x in range(c-1,c+w-1):
                horse_board[y][x] = i
                horse_index[i].append((y,x))

    horse_hp = deepcopy(horse_ori_hp)

    # 왕의 명령만큼 대결 진행
    for i in range(q):
        # 기사의 번호와 이동방향
        horse_num, d = map(int,input().split())

        # 기사 이동
        horse_move_and_fight(horse_num,d)

        # 함정터지기


    ans = 0
    for i in range(len(horse_hp)):
        if horse_hp[i] > 0:
            ans += horse_ori_hp[i] - horse_hp[i]
    print(ans)