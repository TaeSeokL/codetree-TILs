def move_player():
    # [1] 팀 이동 시키기
    for tnum in range(1,len(team)):
        for p in range(1,len(team[tnum])):
            py, px = team[tnum][p]

            if p+1 == len(team[tnum]) :
                for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    flag = False
                    ny = py + dy
                    nx = px + dx

                    if 0 <= ny < n and 0 <= nx < n and board[ny][nx] == -4:
                        for ddy, ddx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                            nny, nnx = ny + ddy, nx + ddx
                            if 0 <= nny < n and 0 <= nnx < n and board[nny][nnx] == board[py][px] - 1:
                                team[tnum][p] = [ny,nx]
                                board[ny][nx], board[py][px] = board[py][px], -4
                                flag = True
                                break

                    if flag:
                        break
            else:
                for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    ny = py + dy
                    nx = px + dx

                    if 0 <= ny < n and 0 <= nx < n and board[ny][nx] == -4:
                        team[tnum][p] = [ny, nx]
                        board[ny][nx], board[py][px] = board[py][px], -4
                        break

def throw_ball(round):
    global ans

    if 1 <= round <= n:  # 오른쪽으로 가는 공
        by, bx = round - 1, 0
        bd = 0
    elif n + 1 <= round <= 2 * n:  # 위쪽으로 가는 공
        by, bx = n - 1, (round - 1) % n
        bd = 1
    elif 2 * n + 1 <= round <= 3 * n:  # 왼쪽으로 가는 공 (거꾸로 처리)
        by, bx = (round - 1) % n, n - 1
        bd = 2
    else:  # 아래쪽으로 가는 공 (거꾸로 처리)
        by, bx = 0, (round - 1) % n
        bd = 3

    # [3] 공이 던져지는 과정 구현
    for _ in range(n - 1):
        if board[by][bx] != 0 and board[by][bx] != -4:  # 사람 발견한 경우
            ans += board[by][bx] ** 2

            # 해당팀 머리 꼬리 바꾸기
            for tnum in range(1,len(team)):
                if [by,bx] in team[tnum]:
                    # 원래 머리 좌표와 꼬리 좌표 구해서 좌표상 위치 바꾸기
                    hy,hx = team[tnum][1]
                    ty,tx = team[tnum][len(team[tnum])-1]
                    board[hy][hx], board[ty][tx] = board[ty][tx], board[hy][hx]

                    # 팀 정보 갱신
                    team[tnum][1], team[tnum][len(team[tnum])-1] = team[tnum][len(team[tnum])-1], team[tnum][1]

                    return
        else:
            by, bx = by + ball_dir[bd][0], bx + ball_dir[bd][1]

if __name__=='__main__':
    n, m, k = map(int,input().split())          # n 격자 크기 / m 팀 갯수 / k 라운드 수

    board = [list(map(int,input().split())) for _ in range(n)]    # 격자 정보
    team = [[] for _ in range(m+1)]
    ball_dir = [(0,1),(-1,0),(0,-1),(1,0)]  # 공 방향 / 우 상 좌 하
    ans = 0

    for r in range(n):
        for c in range(n):
            if board[r][c] == 4 :
                board[r][c] = -4
    t_num = 1
    for r in range(n):
        for c in range(n):
            if board[r][c] == 1:
                y,x = r,c
                pnum = 2
                temp = [0,[y,x]]
                while True:
                    flag = False
                    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                        ny = y + dy
                        nx = x + dx

                        if 0 <= ny < n and 0 <= nx < n and board[ny][nx] != 0 and board[ny][nx] != -4 and [ny,nx] not in temp:
                            board[ny][nx] = pnum
                            temp.append([ny,nx])
                            pnum += 1
                            y, x = ny, nx
                            flag = True
                            break

                    if not flag:
                        break

                team[t_num] = temp
                t_num += 1


    for round in range(1,k+1):
        # [1] 팀 이동
        move_player()

        # [2] 공 던지기 구현
        throw_ball(round)

    print(ans)