from collections import deque
from copy import deepcopy
# 기사 이동 및 대결
# 큰 흐름
# 1. 명령을 받은 말이 명령 방향으로 이동가능한지 확인
    # 1-1. 만약 벽이 있다면 이동 못함. 바로 함수 탈출
    # 1-2. 만약 다른 기사가 있다면 탐색을 이어나가야 하기때문에 기사 번호를 큐에 저장해줌.

# 2. 1에서 찾은 탐색해야하는 기사를 기준으로 똑같은 행위를 큐가 빌때까지 반복해줌.
    # 2-1. 이것도 벽이 있거나, 인덱스 범위를 벗어나면 바로 함수를 종료시킴.

# 3. 실제로 이동해야하는 기사들을 이동시켜줌. 이때 기사들간 겹치면서 horse_board에 업데이트가 제대로 안되는 문제가 있었음.
# 그래서 러프하게 원래있던위치를 0으로 만들고, 새로운 위치값만 제대로 갱신시킨 후에 다시 밑의 반복문에서 horse_board에
# 제대로 업데이트 시켜줌.

# 4. 함정위치를 기준으로 기사들이 있는 공간에 함정칸이 있는지 체크한 뒤 데미지를 입혀줌.

# 5. 죽은 기사들을 horse_board에서 제거시켜줌.

def horse_move_and_fight(num,d):
    dy, dx = dir[d]                 # 이동 방향
    moving_horse = deque()          # 이동가능성이 있는 기사들 저장 큐
    real_moving_horse = deque()     # 실제로 이동해야하는 기사들 저장 큐
    real_moving_horse.append(num)

    # 이동 명령을 받은 기사의 명령 방향으로 벽 or 범위 out 이면 함수 종료
    # 범위 안인데, 자기 자신 아니고, 0 아닐때 == 다른기사 존재 => 다른 기사 기준 탐색 더해야함.
    # 다른 기사 번호 큐에 추가
    for (y,x) in horse_index[num]:
        ny, nx = y+dy, x+dx

        if 0<=ny<l and 0<=nx<l:
            if board[ny][nx] == 2:
                return

            elif horse_board[ny][nx] != num and horse_board[ny][nx] != 0 :
                if horse_board[ny][nx] not in moving_horse: # 중복추가제어
                    moving_horse.append(horse_board[ny][nx])
        else:
            return

    # 다른 기사들을 기준으로 탐색을 이어나감. 위와 똑같이 범위 out or 벽 있으면 바로 함수 종료
    while moving_horse:
        horse_num = moving_horse.popleft()
        real_moving_horse.append(horse_num)

        for (y,x) in horse_index[horse_num]:
            ny, nx = y + dy, x + dx

            if 0 <= ny < l and 0 <= nx < l:
                if board[ny][nx] == 2:
                    return

                elif horse_board[ny][nx] != horse_num and horse_board[ny][nx] != 0:
                    if horse_board[ny][nx] not in moving_horse:
                        moving_horse.append(horse_board[ny][nx])
            else:
                return

    # 실제로 이동하는 기사들의 체력을 깎아야하기 때문에 카피해주고 명령받은 기사만 제거시켜줌.
    demage_horse = deepcopy(real_moving_horse)
    demage_horse.remove(num)

    # 기사들을 이동시켜줌. 여기서 temp는 기사들의 새 위치를 업데이트 하기 위한 임시 배열임.
    # horse_index에 쉽게 접근하기 위해 temp에 저장 후 한번에 싹 업데이트 해줌.
    # 여기서 고민했던건, board를 아예 새로 만들어서 horse_board에 딥카피할까도 생각했지만
    # 배열을 또 생성하고 딥카피하는게 시간이 많이 걸릴거같아서
    # 라인 75 ~ 라인 81 까지의 과정으로 원래 있던 위치를 0으로 모두 만들어주고 새로운 위치에
    # 기사를 업데이트 하는 것으로 진행했음.
    while real_moving_horse:
        horse_num = real_moving_horse.popleft()
        temp = []
        for (y,x) in horse_index[horse_num]:
            ny, nx = y + dy, x + dx
            temp.append((ny,nx))
            horse_board[y][x] = 0
        horse_index[horse_num] = temp

    for i in range(1, len(horse_index)):
        for (y,x) in horse_index[i]:
            horse_board[y][x] = i

    # 데미지를 받아야하는 기사들의 위치 인덱스안에 함정이 있는지 체크함.
    # 함정이 있고, 생존해있다면 체력을 1씩 깎아줌.
    for i in range(len(demage_horse)):
        for y,x in bomb_index:
            if (y,x) in horse_index[demage_horse[i]] and horse_hp[demage_horse[i]] > 0:
                horse_hp[demage_horse[i]] -= 1

    # 죽은 기사들을 horse_board에서 제거해줌. 모두 빈칸으로 만들어주면됨.
    for i in range(1, len(horse_hp)):
        if horse_hp[i] == 0:
            for (y,x) in horse_index[i]:
                horse_board[y][x] = 0

if __name__=='__main__':
    l,n,q = map(int,input().split())                            # l = 맵크기, n = 기사수, q = 왕 명령 수
    board = [list(map(int,input().split())) for _ in range(l)]  # 함정과 벽, 빈칸 배열
    bomb_index = []                                             # 함정 위치 인덱스 배열, 함정위치 찾아주기
    for i in range(l):
        for j in range(l):
            if board[i][j] == 1:
                bomb_index.append((i,j))

    horse_board = [[0]*l for _ in range(l)]     # 기사들 저장할 배열
    horse_index = [[] for _ in range(n+1)]      # 기사 위치 인덱스 배열
    horse_ori_hp = [0]                          # 기사 체력 배열
    dir = [(-1,0),(0,1),(1,0),(0,-1)]           # 이동방향

    # 기사 위치를 표시해줌
    for i in range(1,n+1):
        r,c,h,w,k = map(int,input().split())
        horse_ori_hp.append(k)                  # 기사 체력 저장

        # i = 기사 번호, 각 기사는 사각형태기 때문에
        # y,x 범위를 설정해서 기사의 크기만큼 기사번호를 할당해줌.
        # 기사 위치 관리 인덱스에도 추가해줌.
        for y in range(r-1,r+h-1):
            for x in range(c-1,c+w-1):
                horse_board[y][x] = i
                horse_index[i].append((y,x))

    # 체력에 데미지를 입히기 위해 원본 배열을 놔두고 카피해줌.
    horse_hp = deepcopy(horse_ori_hp)

    # 왕의 명령만큼 대결 진행
    for i in range(q):
        # 기사의 번호와 이동방향
        horse_num, d = map(int,input().split())

        # 기사가 죽었으면 진행 안함.
        if horse_hp[horse_num] == 0:
            continue

        # 기사 이동 및 함정터지기
        horse_move_and_fight(horse_num,d)

    # 정답계산 : 생존한 기사들이 받은 데미지를 합산해서 출력.
    ans = 0
    for i in range(1, len(horse_hp)):
        if horse_hp[i] > 0:
            ans += horse_ori_hp[i] - horse_hp[i]
    print(ans)