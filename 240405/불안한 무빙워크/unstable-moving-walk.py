from collections import deque
if __name__=='__main__':
    n, k = map(int,input().split())                 # n 길이 / k 종료조건
    moving_walk = list(map(int,input().split()))    # 무빙워크
    person = []
    turn = 1
    while True:
        # 무빙워크 한칸 회전
        moving_walk.insert(0,moving_walk.pop())

        # 사람 위치 +1 씩 해주기 : 무빙워크 자체가 회전하는 거기때문에 조건 확인 안해도됨.
        for i in range(len(person)-1,-1,-1):
            ori_pos = person[i]
            new_pos = ori_pos + 1
            if new_pos == n-1:
                person.pop(i)
            else:
                person[i] = new_pos

        # 사람이 이동 : 안전성이 0이 아니고 사람이 없는 경우
        for i in range(len(person)-1,-1,-1):
            ori_pos = person[i]
            new_pos = ori_pos + 1

            if moving_walk[new_pos] > 0:
                if new_pos == n-1:                                          # 내리는 자리 일때
                    person.pop(i)
                    moving_walk[new_pos] -= 1
                elif new_pos not in person :    # 다음칸에 안전성이 충분하고, 사람이 없을때
                    person[i] = new_pos
                    moving_walk[new_pos] -= 1

        # 1번칸에 사람 없고 안전성이 0이상이면 사람 올리기
        if 0 not in person and moving_walk[0] > 0:
            person.insert(0,0)
            moving_walk[0] -= 1

        # 안전성이 0인 칸 k개 이상이면 종료
        res = moving_walk.count(0)
        if res >= k:
            print(turn)
            break

        turn += 1