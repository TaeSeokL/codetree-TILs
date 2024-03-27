def win(num,y,x):
    # 승리한칸에 있는 총들과 자기가 갖고 있는 총중에 가장 쎈거 들기
    temp = gun_arr[y][x] + [player_gun[num]]
    temp.sort(reverse=True)

    player_gun[num] = temp.pop(0)
    gun_arr[y][x] = temp

    # 플레이어 정보 갱신
    _,_,d,s = player[num]
    player[num] = [y,x,d,s]
    player_pos[y][x] = num
    return

def lose(num,y,x):

    # 자기가 갖고 있던 총 격자에 내려두기
    if player_gun[num] != 0:
        gun_arr[y][x].append(player_gun[num])
        player_gun[num] = 0

    # 해당 플레이어가 원래 가지고 있던 방향대로 한칸 가기
    _,_,d,s = player[num]

    for i in range(4):
        dd = (d+i)%4
        ny = y + dir[dd][0]
        nx = x + dir[dd][1]

        if 0<=ny<n and 0<=nx<n and player_pos[ny][nx] == 0 :
            # 플레이어 정보 갱신
            player[num] = [ny,nx,dd,s]
            player_pos[y][x],player_pos[ny][nx] = 0,num

            # 총 있을 경우 획득
            if len(gun_arr[ny][nx]) > 0:
                gun_arr[ny][nx].sort(reverse=True)
                player_gun[num] = gun_arr[ny][nx].pop(0)

            return


if __name__=='__main__':
    n,m,k = map(int,input().split())            # n 격자크기 / m 플레이어수 / k 라운드 수

    # 총 관리 3차원 배열 제작
    gun_arr = [[[] for _ in range(n)] for _ in range(n)]
    temp = [list(map(int,input().split())) for _ in range(n)]
    for r in range(n):
        for c in range(n):
            if temp[r][c] != 0:
                gun_arr[r][c].append(temp[r][c])

    player_pos = [[0]*n for _ in range(n)]      # 선수 위치

    # 플레이어 관리 2차원 배열 제작
    player = [0]                                # 위치 / 방향 / 초기 능력치
    for i in range(1,m+1):
        y,x,d,s = map(int,input().split())
        player.append([y-1,x-1,d,s])
        player_pos[y-1][x-1] = i

    player_gun = [0]*(m+1)              # 선수가 가진 총
    player_point = [0]*(m+1)            # 선수가 얻은 포인트
    dir = [(-1,0),(0,1),(1,0),(0,-1)]   # 방향 / 상 우 하 좌

    # 라운드만큼 게임 진행
    for turn in range(k):
        # [1] 플레이어 이동
        for i in range(1,m+1):
            y,x,d,s = player[i]

            ny = y + dir[d][0]
            nx = x + dir[d][1]

            # [2] 문제 조건 처리
            if 0<=ny<n and 0<=nx<n :                  # 범위내
                player_pos[y][x] = 0
                if player_pos[ny][nx] != 0 :               # 이동 위치에 다른 플레이어 있을때 : 싸우기
                    a_player = i                        # 이동한 플레이어
                    b_player = player_pos[ny][nx]       # 원래 있던 플레이어

                    a_total_stat = player_gun[a_player] + player[a_player][3]   # 총 능력치 2개 구하기
                    b_total_stat = player_gun[b_player] + player[b_player][3]

                    if a_total_stat > b_total_stat:     # a가 이겼을때
                        player_point[a_player] += a_total_stat - b_total_stat
                        lose(b_player, ny, nx)
                        win(a_player,ny,nx)


                    elif a_total_stat < b_total_stat:   # b가 이겼을때
                        player_point[b_player] += b_total_stat - a_total_stat
                        lose(a_player, ny, nx)
                        win(b_player, ny, nx)

                    else:                               # 같을때 -> 초기 능력치만 비교
                        a_stat = player[a_player][3]
                        b_stat = player[b_player][3]

                        if a_stat > b_stat:             # a가 이겼을때
                            player_point[a_player] += a_total_stat - b_total_stat
                            lose(b_player, ny, nx)
                            win(a_player, ny, nx)

                        else:                           # b가 이겼을때
                            player_point[b_player] += b_total_stat - a_total_stat
                            lose(a_player, ny, nx)
                            win(b_player, ny, nx)


                else:                                      # 이동 위치에 아무도 없을때
                    # 플레이어 정보갱신
                    player_pos[y][x], player_pos[ny][nx] = 0,i
                    player[i] = [ny,nx,d,s]

                    if len(gun_arr[ny][nx]) > 0 :               # 이동 위치에 총이 있을때
                        if player_gun[i] != 0:                      # 플레이어가 총 갖고 있을때 : 총교체
                            temp = gun_arr[ny][nx] + [player_gun[i]]
                            temp.sort(reverse=True)

                            player_gun[i] = temp.pop(0)
                            gun_arr[ny][nx] = temp
                        else:                                       # 플레이어가 총 안갖고 있을때 : 총줍기
                            gun_arr[ny][nx].sort(reverse=True)

                            player_gun[i] = gun_arr[ny][nx].pop(0)

            else:                               # 범위밖 -> 방향전환
                d = (d+2)%4

                ny = y + dir[d][0]
                nx = x + dir[d][1]

                # [2] 문제 조건 처리
                if 0 <= ny < n and 0 <= nx < n:  # 범위내
                    player_pos[y][x] = 0
                    if player_pos[ny][nx] != 0:  # 이동 위치에 다른 플레이어 있을때 : 싸우기
                        a_player = i  # 이동한 플레이어
                        b_player = player_pos[ny][nx]  # 원래 있던 플레이어

                        a_total_stat = player_gun[a_player] + player[a_player][3]  # 총 능력치 2개 구하기
                        b_total_stat = player_gun[b_player] + player[b_player][3]

                        if a_total_stat > b_total_stat:  # a가 이겼을때
                            player_point[a_player] += a_total_stat - b_total_stat
                            lose(b_player, ny, nx)
                            win(a_player, ny, nx)


                        elif a_total_stat < b_total_stat:  # b가 이겼을때
                            player_point[b_player] += b_total_stat - a_total_stat
                            lose(a_player, ny, nx)
                            win(b_player, ny, nx)

                        else:  # 같을때 -> 초기 능력치만 비교
                            a_stat = player[a_player][3]
                            b_stat = player[b_player][3]

                            if a_stat > b_stat:  # a가 이겼을때
                                player_point[a_player] += a_total_stat - b_total_stat
                                lose(b_player, ny, nx)
                                win(a_player, ny, nx)

                            else:  # b가 이겼을때
                                player_point[b_player] += b_total_stat - a_total_stat
                                lose(a_player, ny, nx)
                                win(b_player, ny, nx)


                    else:  # 이동 위치에 아무도 없을때
                        player_pos[y][x], player_pos[ny][nx] = 0, i  # 위치 갱신
                        player[i] = [ny, nx, d, s]

                        if len(gun_arr[ny][nx]) > 0:  # 이동 위치에 총이 있을때
                            if player_gun[i] != 0:  # 플레이어가 총 갖고 있을때 : 총교체
                                temp = gun_arr[ny][nx] + [player_gun[i]]
                                temp.sort(reverse=True)

                                player_gun[i] = temp.pop(0)
                                gun_arr[ny][nx] = temp
                            else:  # 플레이어가 총 안갖고 있을때 : 총줍기
                                gun_arr[ny][nx].sort(reverse=True)

                                player_gun[i] = gun_arr[ny][nx].pop(0)



    for i in range(1,m+1):
        print(player_point[i], end= ' ')