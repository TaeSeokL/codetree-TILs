def fight(a_player,b_player):
    # 각 플레이어의 정보 가져오기
    ay,ax,ad,a_init = player[a_player]
    by,bx,bd,b_init = player[b_player]

    # 각 플레이어 총 능력치와 얻게될 포인트
    a_player_total = a_init + player_gun[a_player]
    b_player_total = b_init + player_gun[b_player]
    score = abs(a_player_total-b_player_total)
    winner = loser = 0

    # [1] 총 능력치 비교
    if a_player_total>b_player_total:
        winner = a_player
        loser = b_player
    elif a_player_total < b_player_total:
        winner = b_player
        loser = a_player
    # [2] 초기 능력치 비교
    else:
        if a_init > b_init:
            winner = a_player
            loser = b_player
        elif a_init < b_init:
            winner = b_player
            loser = a_player
    # 이긴사람 점수업뎃
    player_score[winner] += score

    # 어차피 이긴사람이나 진사람이나 좌표나 위치를 업데이트해주어야함. 여기서 원래 위치를 삭제시켜줌
    board[ay][ax] = 0
    board[by][bx] = 0
    return winner, loser

def win(num,ny,nx):
    # [1] 위치처리
    _,_,d,s = player[num]
    player[num] = [ny,nx,d,s]       # 위치 갱신
    board[ny][nx] = num

    # [2] 총 획득 -> 땅에 총이 있을떄만
    if gun[ny][nx]:
        temp = []   # 총저장임시배열
        if player_gun[num] != 0:            # 플레이어가 총 가지고 있다면
            temp.append(player_gun[num])    # 그 총 내려놓기

        temp += gun[ny][nx]                 # 해당칸에 있는 총들도 전부 추가, 없으면 추가 안됨.
        temp.sort(reverse=True)             # 젤쎈순으로 정렬
        player_gun[num] = temp.pop(0)       # 젤쎈총 플레이어주기
        gun[ny][nx] = temp                  # 나머지 총은 격자에 내려두기

def lose(num,ny,nx):
    _,_,d,s = player[num]
    # [1] 전투했던 위치에 총내려두기
    if player_gun[num] != 0:
        gun[ny][nx].append(player_gun[num])
        player_gun[num] = 0

    # [2] 이동
    for i in range(4):
        yy = ny + dir[(d+i)%4][0]
        xx = nx + dir[(d+i)%4][1]
        # 범위내 / 사람없는곳
        if 0<=yy<n and 0<=xx<n and board[yy][xx] == 0:
            if gun[yy][xx]:     # 총 있다면 총 획득
                gun[yy][xx].sort(reverse=True)
                player_gun[num] = gun[yy][xx].pop(0)

            # 위치갱신
            player[num] = [yy,xx,(d+i)%4,s]
            board[yy][xx] = num
            return

if __name__=='__main__':
    n,m,k = map(int,input().split())                            # n 맵크기 / m 사람수 / k 라운드 수
    board = [list(map(int,input().split())) for _ in range(n)]  # 맵정보 / 0 빈칸 나머지 총
    dir = [(-1,0),(0,1),(1,0),(0,-1)]                           # 방향(상우하좌)
    player_gun = [0] * (m + 1)                                  # 플레이어가 가진 총
    player_score = [0]*(m+1)                                    # 플레이어점수

    # 총 정보 3차원 배열에 기록해주기
    gun = [[[] for _ in range(n)] for _ in range(n)]
    for r in range(n):
        for c in range(n):
            if board[r][c] >0 :
                gun[r][c].append(board[r][c])
                board[r][c] = 0

    # 플레이어 정보 저장
    player = [0]
    for num in range(1, m + 1):
        y, x, d, s = map(int, input().split())  # 위치, 방향, 초기능력치
        player.append([y - 1, x - 1, d, s])
        board[y - 1][x - 1] = num

    # 라운드 만큼 게임 진행
    for turn in range(k):
        # [1] 각 플레이어 이동
        for num in range(1,m+1):
            y,x,d,s = player[num]

            ny, nx = y + dir[d][0], x + dir[d][1]       # 다음 위치 이동
            if 0<=ny<n and 0<=nx<n:                     # 격자내일경우
                if board[ny][nx] > 0:                   # 사람이 있을 경우 -> 전투!
                    win_p,lose_p = fight(num,board[ny][nx])
                    lose(lose_p,ny,nx)
                    win(win_p,ny,nx)
                else:                                   # 빈칸일 경우 -> 총획득
                    if gun[ny][nx]:                     # 총 있을떄
                        temp = []  # 총저장임시배열
                        if player_gun[num] != 0:            # 플레이어가 총 가지고 있다면
                            temp.append(player_gun[num])    # 그 총 내려놓기

                        temp += gun[ny][nx]                 # 해당칸에 있는 총들도 전부 추가, 없으면 추가 안됨.
                        temp.sort(reverse=True)             # 젤쎈순으로 정렬
                        player_gun[num] = temp.pop(0)       # 젤쎈총 플레이어주기
                        gun[ny][nx] = temp                  # 나머지 총은 격자에 내려두기

                    # 위치갱신
                    board[y][x] = 0
                    player[num] = [ny,nx,d,s]
                    board[ny][nx] = num

            else:                                       # 아닐경우 : 정반대로 한칸 이동
                d = (d+2)%4                             # 정반대방향 업데이트
                player[num][2] = d
                ny, nx = y + dir[d][0], x + dir[d][1]   # 다음 위치 이동

                if board[ny][nx] > 0:                   # 사람이 있을 경우 -> 전투!
                    win_p, lose_p = fight(num, board[ny][nx])
                    lose(lose_p, ny, nx)
                    win(win_p, ny, nx)
                else:                                   # 빈칸일 경우 -> 총획득
                    if gun[ny][nx]:                     # 총 있을떄
                        temp = []  # 총저장임시배열
                        if player_gun[num] != 0:            # 플레이어가 총 가지고 있다면
                            temp.append(player_gun[num])    # 그 총 내려놓기

                        temp += gun[ny][nx]                 # 해당칸에 있는 총들도 전부 추가, 없으면 추가 안됨.
                        temp.sort(reverse=True)             # 젤쎈순으로 정렬
                        player_gun[num] = temp.pop(0)       # 젤쎈총 플레이어주기
                        gun[ny][nx] = temp                  # 나머지 총은 격자에 내려두기

                    # 위치갱신
                    board[y][x] = 0
                    player[num] = [ny, nx, d, s]
                    board[ny][nx] = num

    # 정답 출력
    for num in range(1,m+1):
        print(player_score[num],end= ' ')