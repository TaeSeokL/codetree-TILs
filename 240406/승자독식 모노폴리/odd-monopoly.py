def move_player():
    for i in range(len(player)):
        num,y,x,d = player[i]
        mdir = player_dir[num][d]

        # 빈칸 먼저 검사
        for dd in mdir:
            ny = y + dir[dd][0]
            nx = x + dir[dd][1]
            if 0<=ny<n and 0<=nx<n and board[ny][nx] == 0:
                player[i] = [num,ny,nx,dd]
                break
        else:
            # 자기 땅 검사
            for dd in mdir:
                ny = y + dir[dd][0]
                nx = x + dir[dd][1]
                if 0<=ny<n and 0<=nx<n and board[ny][nx][0] == num:
                    player[i] = [num,ny,nx,dd]
                    break

    # 겹친 플레이어 삭제
    player.sort(key=lambda x: (x[1], x[2]))
    for i in range(len(player) - 1, 0, -1):
        if (player[i][1], player[i][2]) == (player[i - 1][1], player[i - 1][2]):
            player.pop(i)

    player.sort(key=lambda x:x[0])
    # 최종적으로 이동한 곳 계약
    for i in range(len(player)):
        num,y,x,d = player[i]
        board[y][x] = [num,k]

if __name__=='__main__':
    n, m, k = map(int,input().split())                          # n 맵크기 / m 플레이어 수 / k 독점계약턴수
    board = [list(map(int,input().split())) for _ in range(n)]  # 초기 격자 정보
    dir = [0,(-1,0),(1,0),(0,-1),(0,1)]                         # 방향 (상 하 좌 우)

    # 플레이어 정보 저장 [번호,행,열,방향]
    player = []
    for r in range(n):
        for c in range(n):
            if board[r][c] != 0:
                player.append([board[r][c],r,c])
                board[r][c] = [board[r][c],k]
    player.sort(key=lambda x:x[0])

    init_d = list(map(int,input().split()))     # 초기방향 저장
    for i in range(m):
        player[i].append(init_d[i])

    # 플레이어 방향에 따른 이동 우선순위 저장
    player_dir = [[0] for _ in range(m+1)]
    for i in range(1,m+1):
        for _ in range(4):
            ll = list(map(int,input().split()))
            player_dir[i].append(ll)

    turn = 1
    while turn < 1000:
        # 독점 계약 턴 수 줄이기
        for r in range(n):
            for c in range(n):
                if board[r][c] != 0:
                    if board[r][c][1] == 1:
                        board[r][c] = 0
                    else:
                        board[r][c][1] -= 1

        # 플레이어 이동
        move_player()

        # 1만 살았는지 확인
        if len(player) == 1:
            print(turn)
            exit(0)

        turn += 1

    print(-1)