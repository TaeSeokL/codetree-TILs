# 모법 코드

# 플레이어들을 이동시켜주는 함수 -> 술래와의 거리 계산 후 3이하인 사람들만 이동시키기
def move_player():
    for i in range(len(player)):
        py, px, pd = player[i]                      # 플레이어 정보 받기

        dis = abs(ny-py) + abs(nx-px)                 # 술래와의 거리 계산

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
    dir = [(-1,0),(0,1),(1,0),(0,-1)]           # 토네이도 이동 배열 (상 우 하 좌)
    ny,nx = n//2, n//2                          # 술래 초기 위치
    max_cnt,cnt,flag,d,val = 1, 0, 0, 0, 1      # 토네이도 시작 전 초기화

    for turn in range(1,k+1):
        # [1] 플레이어 이동
        move_player()

        # [2] 술래 이동
        cnt += 1
        ny = ny + dir[d][0]
        nx = nx + dir[d][1]

        if (ny, nx) == (0, 0):                              # 1. 밖에서 안으로 들어가는 토네이도로 전환 시점
            max_cnt, cnt, flag, d, val = n, 1, 1, 2, -1
        elif (ny, nx) == (n // 2, n // 2):                  # 2. 안에서 밖으로 나가는 토네이도로 전환 시점
            max_cnt, cnt, flag, d, val = 1, 0, 0, 1, 1
        else:                                               # 3. 둘 다 아닐때는 그냥 하던데로 이동
            if cnt == max_cnt:
                d = (d + val) % 4
                cnt = 0

                if flag == 1:   # flag = 1이면 총 이동거리를 갱신해주고 flag 초기화
                    max_cnt += val
                    flag = 0
                else:           # flag = 0이면 다음 차례때는 총 이동거리 갱신해줘야 하니 flag 1로 만듬
                    flag = 1

        # [3] 감시 시작
        start_catch(ny, nx, d)

        # [4] 플레이어 다 잡혔는지 확인
        if not player:
            break

    print(ans)