from collections import deque

def find_attacker():
    temp = []                       # 공격자와 대상자 후보들 넣기 : [행,열,공격력,최근공격턴,행과열의합]
    for r in range(n):
     for c in range(m):
        if board[r][c] > 0 :
            temp.append([r,c,board[r][c],attack_board[r][c],r+c])

    # 다중정렬을 통해 공격자와 대상자 찾기
    # 공격자 : 공격력이 가장 약한 -> 가장 최근에 공격한 -> 행과열의 합이 가장 큰 -> 열이 가장 큰 // 대상자는 정확히 반대
    temp.sort(key= lambda x:(x[2],-x[3],-x[4],-x[1]))

    ay, ax,_,_,_ = temp[0]    # 공격자
    py, px,_,_,_ = temp[-1]   # 대상자

    # 공격자 정보 업데이트
    board[ay][ax] += n+m            # 공격력
    attack_board[ay][ax] = turn     # 최근 공격 턴

    return ay,ax,py,px

def find_shortcut(ay,ax,py,px):
    dq = deque()                            # 탐색큐 : 현재 탐색 위치와 현재까지 탐색 경로를 저장
    check = [[0]*m for _ in range(n)]       # 방문 배열

    dq.append((ay,ax,[(ay,ax)]))

    while dq:
        y,x,road = dq.popleft()

        # 우 하 상 좌 순으로 탐색(방향우선순위)
        for dy, dx in ((0,1),(1,0),(-1,0),(0,-1)):
            # 행과 열 연결 구현
            ny = (y + dy)%n
            nx = (x + dx)%m

            # 범위 체크 할 필요 없음. 방문안했고, 포탑 안부서진곳만 갈 수 있음.
            if check[ny][nx] == 0 and board[ny][nx] > 0:
                if (ny,nx) == (py,px):      # 대상자에 도달했을때 -> 경로 리턴
                    return road
                else:                       # 아닐때 계속 탐색.
                    dq.append((ny,nx,road+[(ny,nx)]))
    # 경로 없으면 그냥 리턴
    return

if __name__=='__main__':
    n, m, k = map(int,input().split())                            # nxm격자크기 / k 턴수
    board = [list(map(int,input().split())) for _ in range(n)]    # 초기 맵정보

    attack_board= [[0]*m for _ in range(n)]                       # 포탑별 젤 최근에 공격한 턴 저장 배열

    # 턴만큼 게임진행
    for turn in range(1,k+1):
        # [1] 공격자와 대상자 찾기
        ay,ax, py,px = find_attacker()
        related_attack = [(ay,ax),(py,px)]  # 공격에 관여한 포탑 저장

        # [2] 공격 진행
        # [2-1] 공격자와 대상자 간 최단거리 찾기
        shortcut = find_shortcut(ay,ax,py,px)
        # [2-2] 최단거리 존재 시 레이저 공격
        if shortcut:
            # 대상자 우선 공격
            board[py][px] -= board[ay][ax]
            # 경로에 있는 애들 공격 -> 젤 처음에 있는 공격자 제외
            for i in range(1,len(shortcut)):
                y,x = shortcut[i]
                board[y][x] -= board[ay][ax]//2

            # 공격에 관여한 포탑 저장
            related_attack += shortcut[:]

        # [2-3] 최단거리 없을 시 포탄 공격
        else:
            # 대상자 우선 공격
            board[py][px] -= board[ay][ax]
            # 인접한 8방향 공격
            for dy,dx in ((-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)):
                ny = (py + dy)%n
                nx = (px + dx)%m

                # 공격자 아니고 살아남은 포탑이면 공격
                if (ny,nx) != (ay,ax) and board[ny][nx] > 0:
                    board[ny][nx] -= board[ay][ax]//2
                    related_attack.append((ny,nx))
        # [3] 포탑이 1개남았는지 확인 / 공격과 무관한 포탑들 정비 : 공격력 + 1
        cnt = 0
        for r in range(n):
            for c in range(m):
                if board[r][c] < 0 :    # 공격당해서 음수된 애들 0 으로 처리
                    board[r][c] = 0
                if board[r][c] > 0:     # 살아남은애들 처리
                    cnt += 1
                    if (r,c) not in related_attack:
                        board[r][c] += 1
        # 하나남았으면 종료
        if cnt == 1:
            break

    # 살아남은 포탑 중 최대 공격력 구하기 = 정답
    ans = 0
    for r in range(n):
        ans = max(ans,max(board[r]))
    print(ans)