# 이 문제 술래의 위치를 처리하는게 아주 골치가 아프다.
# 달팽이 형태로 나왔다가 다시 들어가는 경로를 무한히 반복하는데 나같은 경우
# [1] (n//2,n//2) -> (0,0) [2] (0,0) -> (n-1,0) [3] (n-1,0) -> (n//2,n//2)
# 위 세가지 경로로 나누어서 처리했다.

# 플레이어들을 이동시켜주는 함수 -> 술래와의 거리 계산 후 3이하인 사람들만 이동시키기
def move_player():
    for i in range(len(player)):
        py, px, pd = player[i]                      # 플레이어 정보 받기

        dis = abs(y-py) + abs(x-px)                 # 술래와의 거리 계산

        if dis <= 3:
            npy = py + player_dir[pd][0]
            npx = px + player_dir[pd][1]

            if 0 <= npy < n and 0 <= npx < n:       # 범위내이고
                if (npy, npx) != (y, x):            # 술래가 없을때만 이동
                    player[i] = [npy, npx, pd]
            else:                                   # 범위 밖일땐 -> 정반대 방향으로 반전
                if pd == 1:
                    pd = 2
                elif pd == 2:
                    pd = 1
                elif pd == 3:
                    pd = 4
                else:
                    pd = 3

                npy = py + player_dir[pd][0]
                npx = px + player_dir[pd][1]

                if 0 <= npy < n and 0 <= npx < n:   # 범위내이고
                    if (npy, npx) != (y, x):        # 술래가 없을때만 이동
                        player[i] = [npy, npx, pd]
                    else:                           # 술래가 있을때 이동은 안하지만, 방향이 바뀌었기때문에, 정보를 갱신해준다.
                        player[i] = [py,px,pd]

# 술래가 감시를 하는 함수
def start_catch(y,x,d):
    global ans

    # temp = 술래가 도망자를 잡을 수 있는 위치 배열 -> 현재 칸 + 바라보는 방향 2칸
    temp = [(y, x)]
    for _ in range(2):
        y, x = y + dir[d%4][0], x + dir[d%4][1]
        if 0 <= y < n and 0 <= x < n:
            temp.append((y, x))

    # 도망자 한명씩 꺼내면서 temp 안에 위치하는지 확인 그리고 나무 없는지 확인
    cnt = 0
    for i in range(len(player) - 1, -1, -1):
        py, px, pd = player[i]
        if (py, px) in temp and (py, px) not in tree:
            player.pop(i)
            cnt += 1

    # 정답 갱신
    ans += cnt * turn

if __name__=='__main__':
    n,m,h,k = map(int,input().split())          # n 격자 크기 / m 도망자 수 / h 나무 수 / k 턴수
    player = []                                 # 플레이어 배열 [y,x,방향]
    player_dir = [0,(0,-1),(0,1),(-1,0),(1,0)]  # 플레이어 방향 (1,2,3,4) = (좌,우,상,하)
    tree = []                                   # 나무 위치 배열
    ans = 0                                     # 정답변수

    # 플레이어 정보 입력 받기.
    # d = 1 이면 좌우로만 이동하는 사람 / d = 2이면 상하로만 이동하는 사람
    for _ in range(m):
        y,x,d = map(int,input().split())
        if d == 1:
            player.append([y-1,x-1,2])
        else:
            player.append([y-1,x-1,4])

    # 나무 위치 저장
    for _ in range(h):
        y,x = map(int,input().split())
        tree.append((y-1,x-1))

    # 술래 이동을 위한 변수들
    dir = [(-1,0),(0,1),(1,0),(0,-1)]   # 토네이도 이동 배열 (상 우 하 좌)
    y,x = n//2, n//2                    # 술래 초기 위치
    length = 2                          # 술래가 이동하는 총 길이 : 2 -> 4 -> 6
    # step = length//2일때 방향전환
    # step = length 일때 방향전환, length 길이 증가
    step = 0
    flag = 0                            # length 증가해야하는지 판단하는 flag
    d = 0                               # 초기 방향 (상)
    turn = 1                            # 게임 진행 턴수
    
    # 무한루프 속 무한루프 -> 1. 턴이 끝나거나 2. 플레이어가 모두 잡혀야만 게임 종료
    while True:
        # 바깥쪽으로 나가는 달팽이 (n//2,n//2) -> (0,0)
        while True:
            # [1] 도망자 이동
            move_player()

            # [2] 술래 이동
            ny = y + dir[d%4][0]
            nx = x + dir[d%4][1]

            # step이 length까지 증가
            step += 1
            if step == length // 2:     # 절반 왔을때 방향전환
                d += 1
            elif step == length :       # 다 도착하면 방향전환, length 길이 늘리기 위해 flag 선언, step 초기화
                d += 1
                step = 0
                flag = 1
            if flag == 1:               # flag 선언됐으면 length 늘려주고 flag 초기화
                length += 2
                flag = 0

            y, x = ny,nx                # 위치 갱신

            # [3] 여기 까지 술래가 이동을 완료한 상태
            if (y,x) == (0,0):          # (0,0)에 오면 방향이 갱신 안되기 때문에 아래를 보도록 조정해줌.
                d = 2

            # [4] 술래잡기 시작
            start_catch(y,x,d)

            if not player:              # 플레이어 다 죽었는지 확인
                print(ans)
                exit(0)

            turn += 1                   # 턴수 늘리기

            if (y,x) == (0,0):          # (0,0)까지 가면 첫번째 루트는 종료되기 때문에 처음 while문 종료
                break

            if turn == k + 1 :          # 턴이 끝나면 게임 종료
                print(ans)
                exit(0)

        # 일직선 달팽이 (0,0) -> (n-1,0)
        while True:
            # [1] 도망자 이동
            move_player()

            # [2] 술래이동
            ny = y + dir[d][0]
            nx = x + dir[d][1]

            y, x = ny,nx

            if (y,x) == (n-1,0):        # (n-1,0)에서 방향 갱신 안되기 때문에 오른쪽을 보도록 조정해줌
                d = 1

            # [3] 술래잡기 시작
            start_catch(y,x,d)

            if not player:              # 플레이어 다 죽었는지 확인
                print(ans)
                exit(0)

            turn += 1                   # 턴수 늘리기

            if (y,x) == (n-1,0):        # (n-1,0)에서 다음 탐색을 위해 파라미터 초기화
                length = 2 * n - 2      # 말려들어가는 달팽이는 아까랑 반대로 length가 줄어들어야함
                step = 0
                flag = 0
                break

            if turn == k + 1 :          # 턴 끝나면 게임 종료
                print(ans)
                exit(0)

        # 말려들어가는 달팽이 (n-1,0) -> (n//2, n//2)
        while True:
            # [1] 도망자 이동
            move_player()

            # [2] 술래 이동
            ny = y + dir[d%4][0]
            nx = x + dir[d%4][1]

            step += 1

            if step == length//2:       # 절반 왔을때 반시게 회전
                d -= 1
            elif step == length:        # 다 왔을때 반시계 회전 및 length 조정을 위한 flag 선언
                d -= 1
                step = 0
                flag = 1

            if flag == 1:               # flag가 있을때 length 줄여주기
                length -= 2
                flag = 0

            y, x = ny ,nx               # 위치 갱신

            if (y,x) == (n//2,n//2):    # 정중앙에 왔을때 방향 갱신 안되기 때문에 위를 보도록 조정
                d = 0

            # [3] 술래잡기 시작
            start_catch(y, x,d)

            if not player:              # 플레이어 다 죽었는지 확인
                print(ans)
                exit(0)

            turn += 1                   # 턴수 늘리기

            # 여기까지 달팽이를 나갔다가 들어오는 한사이클이 완료된 것. 하지만 턴이 아직 남았거나
            # 게임이 끝날 조건이 안됐을 경우, 또 다음 사이클을 반복하기 위해 파라미터를 초기화(처음과 동일)
            if (y,x) == (n//2,n//2):
                length = 2
                step = 0
                flag = 0
                break
                
            if turn == k + 1 :          # 턴이 끝나면 게임 종료
                print(ans)
                exit(0)