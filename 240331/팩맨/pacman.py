# 백준 23290과 똑같은 문제임
# 배울만한 개념
# 1. 범위 처리를 바운더리로 한 것 (not in, in 사용)
# 2. 이동경로 구하기를 재귀말고 3중 for문으로 구현
# 3. 이동경로 중복을 제거하기 위해 set 자료형을 사용
# 4. 몬스터를 군집화시켜서 시간을 줄임.

def move_monster():
    # 물고기 군집 꺼내서 이동시켜주기
    for i in range(len(monster)):
        y,x,d,num = monster[i]

        for k in range(8):
            ny, nx = y + monster_dir[(d+k)%8][0], x + monster_dir[(d+k)%8][1]
            # 범위 내이고, 팩맨이 없고, 시체가 없을때
            if (ny,nx) in boundary and (ny,nx) != (py,px) and monster_body[ny][nx] == 0:
                monster[i] = [ny,nx,(d+k)%8,num]
                break

def move_packman():
    global py,px
    max_eat_monster = -1    # 잡아먹은 몬스터 최대 갯수
    del_road = set()        # 최종 이동할 경로

    # 3중 for문을 통해 이동 가능한 경로 구하기 / (상 좌 하 우) 우선순위로 이동
    for d1 in (0,2,4,6):
        r1, c1 = py + monster_dir[d1][0], px + monster_dir[d1][1]
        if (r1,c1) not in boundary:     continue
        for d2 in (0,2,4,6):
            r2, c2 = r1 + monster_dir[d2][0], c1 + monster_dir[d2][1]
            if (r2, c2) not in boundary:     continue
            for d3 in (0, 2, 4, 6):
                r3, c3 = r2 + monster_dir[d3][0], c2 + monster_dir[d3][1]
                if (r3, c3) not in boundary:     continue

                # 팩맨이 이동할 수 있는 경로를 다 구한 상황
                pack_road = set(((r1,c1),(r2,c2),(r3,c3)))
                eat_monster = 0

                # 몬스터 군집 검사하면서 이 경로에 포함되는지 확인
                for i in range(len(monster)):
                    y,x,d,num = monster[i]

                    # 잡아먹는 몬스터 갯수 구하기
                    if (y,x) in pack_road:
                        eat_monster += num

                # 최대로 먹을 수 있는 경로를 구했을때 / 나중에 삭제해줄 물고기 위치를 저장해줌 / 팩맨 좌표도 저장해줌
                if eat_monster > max_eat_monster:
                    max_eat_monster = eat_monster
                    del_road = pack_road
                    yy, xx = r3,c3

    # 몬스터 삭제해주고 냄새남겨주기
    for i in range(len(monster) -1, -1,-1):
        if (monster[i][0],monster[i][1]) in del_road:
            monster_body[monster[i][0]][monster[i][1]] = 3
            monster.pop(i)

    return yy,xx

def merge_monster():
    # 위치와 방향이 같은 몬스터들을 군집화해준다.
    # 같은 좌표 같은 방향으로 우선 정렬
    monster.sort(key=lambda x:(x[0],x[1],x[2]))

    # 거꾸로 돌면서 그 전 꺼와 위치와 방향이 같다면 갯수 합쳐주기
    for i in range(len(monster)-1,0,-1):
        if monster[i][:3] == monster[i-1][:3]:
            monster[i-1][3] += monster[i][3]
            monster.pop(i)

if __name__ == '__main__':
    m, t = map(int,input().split())         # m 몬스터 수 / t 턴수
    py, px = map(int,input().split())       # 팩맨의 초기 위치
    py, px = py -1, px -1

    monster = []                            # 몬스터 군집화 배열
    for _ in range(m):
        r,c,d = map(int,input().split())    # 몬스터들의 위치와 방향
        monster.append([r-1,c-1,d-1,1])     # [행,열,방향,갯수] 형태로 저장

    monster_dir = [(-1,0),(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1)]   # 몬스터 방향
    boundary = set([(i,j) for j in range(4) for i in range(4)])             # 범위 바운더리 제작
    monster_body = [[0]*4 for _ in range(4)]                                # 몬스터 시체
    # 턴수만큼 게임 진행
    for turn in range(t):
        # [1] 몬스터 복제 시도
        copy_monster = [x[:] for x in monster]     # 나중에 더해줌

        # [2] 몬스터 이동
        move_monster()

        # [3] 팩맨 이동
        py,px = move_packman()

        # [4] 몬스터 시체 소멸
        for r in range(4):
            for c in range(4):
                if monster_body[r][c] > 0:
                    monster_body[r][c] -= 1

        # [5] 몬스터 복제 완성
        monster += copy_monster

        # [5] 몬스터 군집화
        merge_monster()

    ans = 0
    for i in range(len(monster)):
        ans += monster[i][3]

    print(ans)