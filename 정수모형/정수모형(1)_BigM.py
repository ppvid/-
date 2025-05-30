from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
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

from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
#예제2_BigM 활용 (Either-Or/K out of N 제약 조건이 일 때 사용 용이)
#의사결정 변수: 생산 시간
# x1:공장1-장난감1, x2:공장1-장난감2
#x3:공장2-장난감1, x4:공장2-장난감2
x={}
for i in range(4):
    x[i]=solver.NumVar(0,solver.infinity(),'x[%i]'%i)

#공장 선택 제약조건(Either-Or, 둘 중 하나 선택)
y=solver.BoolVar('y')
M=1000000
#y가 0이면 공장 1 가동, y가 1이면 공장2 가동
solver.Add(x[0]+x[1]<=M*(1-y))
solver.Add(x[2]+x[3]<=M*y)

#장난감 생산 제약조건(K out of N, 결정 변수 여러개 생성)
z={}
for i in range(2):
    z[i]=solver.BoolVar('z[%i]'%i)
solver.Add(x[0]+x[2]<=M*z[0])
solver.Add(x[1]+x[3]<=M*z[1])
#생산 시간 제약식 설정
solver.Add(x[0]+x[1]<=500)
solver.Add(x[2]+x[3]<=700)
#목적함수 설정
solver.Maximize(10*(50*x[0]+40*x[2])+15*(40*x[1]+25*x[3])-50000*z[0]-80000*z[1])

status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(solver.Objective().Value())
    for i in range(4):
        print(x[i].name(),':',x[i].solution_value())

#매번 solver를 다시 선정해주지 않으면 값이 누적되어 충돌한다.
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
#예제3. 할당문제(화재 대응 시간 최소화)
data=[[5,12,30,20,15],
      [20,4,15,10,25],
      [15,20,6,15,12],
      [25,15,25,4,10],
      [10,25,15,12,5]
]
avg=[2,1,3,1,3]
x={}
#i:소방서 설치 구역 j:할당 지역
for i in range(5):
    for j in range(5):
        x[i,j]=solver.BoolVar('x[%i,%i]'%(i,j))
#두개의 소방서 제약조건(k out of N)
y={}
for i in range(5):
    y[i]=solver.BoolVar('y[%i]'%i)
M=1000000
for i in range(5):
    solver.Add(sum(x[i,j] for j in range(5))<=M*y[i])
solver.Add(sum(y[i] for i in range(5)) ==2)
#모든 구역 한개의 소방서 할당
for j in range(5):
    solver.Add(sum(x[i,j] for i in range(5))==1)
#목적함수 작성하기
obj=solver.Objective()
for i in range(5):
    for j in range(5):
        obj.SetCoefficient(x[i,j],data[i][j]*avg[j])
obj.SetMinimization()

status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(obj.Value())
    for i in range(5):
        for j in range(5):
            if x[i,j].solution_value() !=0:
                print(x[i,j].name(),':',x[i,j].solution_value())
    for i in range(5):
        print(y[i].name(),':',y[i].solution_value())
