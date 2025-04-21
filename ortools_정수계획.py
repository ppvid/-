from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SAT')

#예제1
#대구, 광주 중 하나 또는 두 곳에 다 새로운 공장(factory)을 세우려고 한다.
#제조품 저장을 위한 창고(warehouse)도 공장이 세워지는 장소에 하나만
cost=[60,30,50,20]
value=[90,50,60,40]
limit=110
#의사결정 변수
x={}
for i in range(4):
    x[i]=solver.BoolVar('x[%i]'%i)
#solver.Add(x[0]+x[1]<=2) 두 변수 다 이진변수이기 때문에 최댓값은 2, 아무 제약을 걸지 않는 코드이다.
solver.Add(x[2]+x[3]<=1,'const1') #제약 조건의 이름을 붙일 수 있다
solver.Add(x[2]<=x[0],'const2') #x[0]에 공장이 설립 됐을 시에 x[3]에 창고 설립 가능능
solver.Add(x[3]<=x[1],'const3') #
solver.Add(sum(cost[i]*x[i] for i in range(len(cost))) <=110,'const4')
solver.Maximize(sum(value[i]*x[i] for i in range(len(value))))

with open('5_1','w') as out_f:#파일 생성(파일 이름: 5_1)
    lp_text=solver.ExportModelAsLpFormat(False)#선형계획법 모델 작성 코드
    out_f.write(lp_text)#생성한 파일에 문제 모델 입력, 파일 열면 목적함수, 제약식 등 확인 가능
status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(solver.Objective().Value())
    for i in range(len(x)):
        print(x[i].name(),':',x[i].solution_value())
