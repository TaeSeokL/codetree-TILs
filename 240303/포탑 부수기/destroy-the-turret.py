from copy import deepcopy
from collections import deque

def find_min_road(ay,ax,dy,dx):
    global min_road
    check = [[0] * m for _ in range(n)]
    dq = deque()
    dq.append((ay,ax,[]))
    check[ay][ax] = 1

    while dq:
        y,x,road = dq.popleft()

        if y == dy and x == dx :
            min_road = deepcopy(road)
            return

        for yy, xx in ((0,1),(1,0),(0,-1),(-1,0)):
            ny, nx = y + yy, x + xx

            ny,nx = ny%n, nx%m
            if board[ny][nx] > 0 and check[ny][nx] == 0:
                dq.append((ny,nx,road + [(ny,nx)]))
                check[ny][nx] = 1

if __name__=='__main__':
    n, m, k = map(int,input().split())          # n x m 격자 크기, k 턴 수

    board = [list(map(int,input().split())) for _ in range(n)]  # 맵정보
    attack_turn = [[0]*m for _ in range(n)]                     # 포탑별 최근 공격한 턴 저장
    total_potop = 0

    for r in range(n):
        for c in range(m):
            if board[r][c] != 0:
                total_potop += 1

    # 턴수만큼 반복
    for turn in range(1,k+1):

        # 공격자와 피해자 선정 : 완전 탐색 + 다중정렬
        # 공격자, 피해자 후보들 저장배열
        temp = []
        related_attack = []  # 공격에 영향 받은 포탑들 위치
        for r in range(n):
            for c in range(m):
                if board[r][c] != 0:
                    temp.append((r,c,r+c,board[r][c],attack_turn[r][c]))
        # 후보들을 우선순위 기준으로 정렬
        # 공격력 가장 낮은 -> 가장 최근에 공격 -> 행과 열 합이 가장 큰 -> 열이 가장 큰
        temp.sort(key=lambda x:(x[3],-x[4],-x[2],-x[1]))

        # 정렬 후 맨앞이 공격자, 맨 뒤가 피해자
        attack_y, attack_x,_,_,_ = temp[0]
        board[attack_y][attack_x] += n+m
        attack_turn[attack_y][attack_x] = turn
        related_attack.append((attack_y,attack_x))

        damage_y, damage_x,_,_,_ = temp[-1]
        related_attack.append((damage_y,damage_x))

        # 최단경로 찾기
        min_road = []
        find_min_road(attack_y,attack_x,damage_y,damage_x)

        # 최단 경로 존재 => 레이저 공격 / 존재 안함 -> 포탄 공격
        if min_road:
            # 경로에 있는 놈들 공격
            for i in range(len(min_road)-1):
                ry, rx = min_road[i]
                if board[ry][rx] > 0 :
                    board[ry][rx] -= board[attack_y][attack_x]//2
                    related_attack.append((ry,rx))
                    if board[ry][rx] <= 0:
                        board[ry][rx] = 0
                        total_potop -= 1

            board[damage_y][damage_x] -= board[attack_y][attack_x]
        else:
            board[damage_y][damage_x] -= board[attack_y][attack_x]
            # 8방향 데미지
            for dy,dx in ((-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)):
                ny, nx = damage_y + dy, damage_x + dx
                ny, nx = ny%n, nx%m

                if (ny,nx) != (attack_y,attack_x) and board[ny][nx] > 0:
                    related_attack.append((ny,nx))
                    board[ny][nx] -= board[attack_y][attack_x]//2
                    if board[ny][nx] <= 0:
                        board[ny][nx] = 0
                        total_potop -= 1

        if board[damage_y][damage_x] <= 0:
            board[damage_y][damage_x] = 0
            total_potop -= 1

        # 포탑 부수기 : 여기서 살아남은 포탑 갯수 확인하기, 1개만 살아있다면 게임 종료
        if total_potop == 1:
            for r in range(n):
                for c in range(m):
                    if board[r][c] != 0:
                        print(board[r][c])
                        exit(0)

        # 포탑 정비
        for r in range(n):
            for c in range(m):
                if board[r][c] != 0 and (r,c) not in related_attack:
                    board[r][c] += 1


    max_val = -100
    for x in board:
        row_max_val = max(x)
        max_val = max(max_val,row_max_val)
    print(max_val)