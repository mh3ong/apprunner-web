import math
# lambda vs app runner cost comparison
# The region is us-east-1 (Virginia).
###
#Default Scenario : 최소한으로 구성 -> vCPU 1개 사용, 메모리 1024MB 사용 (App Runner는 최소 2048MB)
#                 -> 1초에 100건까지 하나의 Instance(1vCPU, 2GB RAM)에서 처리 가능으로 가정
#

###
# 받아야 하는 인자 값들
# - 초당 요청 수
# - lambda 평균 응답속도
# - lambda arm 여부
print("### Lambda Configuration ###")
requestsPerSecond = int(input("Request per second : "))
aveargeLambdaDurationMs = int(input("Average lambda duration (ms) : "))
# applicationMemory = int(input("Application memory : "))
applicationMemory = 1024
lambdaArchitectureIsIntel = bool(int(input("1 -> Intel / 0 -> ARM : ")))
print("### App Runner Configuration ###")
isTrafficDiffrentInPeakTime = bool(int(input("Is the number of traffic requests number diffrent from peak times? \n 1 -> true / 0 -> false : ")))
if (isTrafficDiffrentInPeakTime):
  peakTrafficHours = int(input("Peak traffic hours : "))
  peakRequestsPerSecond = int(input("Peak time requests per second : "))
  nonPeakRequestsPerSecond = abs(peakRequestsPerSecond - requestsPerSecond)

monthSeconds = 60 * 60 * 24 * 30

def calcLambdaComputeCharge(requestsPerSecond, aveargeLambdaDurationMs, applicationMemory, lambdaArchitectureIsIntel):
  if (lambdaArchitectureIsIntel):
    computeCharges = 0.0000166667
  else:
    #ARM Architecture
    computeCharges = 0.0000133334
  # miliseconds x monthSeconds x requestsperSecond / milisecond Translation
  totalComputeSeconds = aveargeLambdaDurationMs * monthSeconds * requestsPerSecond / 1000
  # Free-tier 400,000GB/s
  totalComputeGBs = (totalComputeSeconds * applicationMemory / 1024) - 400000
  if (totalComputeGBs <= 400000):
    totalComputeCharges = 0
  else:
    totalComputeCharges = totalComputeGBs * computeCharges
  return totalComputeCharges
  
def calcLambdaRequestCharge(monthlyRequests):
  # free tier 1M requests
  requestCharge = monthlyRequests - 1000000
  # 1M -> 0.2 USD 1 -> 0.0000002
  totalCharge = requestCharge * 0.0000002
  return totalCharge

def calcAppRunnerCharge(requestsPerSecond, peakTime=24):
  # One Instance can be processing only 100 requests.
  instanceNumber = math.ceil(requestsPerSecond / 100)
  # default memory size is 2048MB
  computingMemoryTime = instanceNumber * peakTime * 2
  totalComputingMemoryCharge = computingMemoryTime * 0.007
  computingVCPUTime = instanceNumber * peakTime
  totalComputingVCPUCharge = computingVCPUTime * 0.064
  totalCharge = (totalComputingMemoryCharge + totalComputingVCPUCharge) * 30
  return totalCharge

def calcPeakAppRunnerCharge(peakTrafficHours, peakRequestsPerSecond, nonPeakRequestsPerSecond):
  totalPeakAppRunnerCharge = calcAppRunnerCharge(peakRequestsPerSecond, peakTrafficHours)
  print(totalPeakAppRunnerCharge)
  totalNonPeakAppRunnerCharge = calcAppRunnerCharge(nonPeakRequestsPerSecond, abs(24-peakTrafficHours))
  print(totalNonPeakAppRunnerCharge)
  totalCharge = totalPeakAppRunnerCharge + totalNonPeakAppRunnerCharge
  return totalCharge

totalLambdaComputeCharges = calcLambdaComputeCharge(
  requestsPerSecond=requestsPerSecond,
  aveargeLambdaDurationMs=aveargeLambdaDurationMs,
  applicationMemory=applicationMemory,
  lambdaArchitectureIsIntel=lambdaArchitectureIsIntel
  )
totalLambdaRequestCharges = calcLambdaRequestCharge(
  monthlyRequests=monthSeconds*requestsPerSecond
)

totalLambdaCharges = totalLambdaComputeCharges + totalLambdaRequestCharges

if (isTrafficDiffrentInPeakTime):
  totalAppRunnerCharges = calcPeakAppRunnerCharge(
    peakTrafficHours=peakTrafficHours,
    peakRequestsPerSecond=peakRequestsPerSecond,
    nonPeakRequestsPerSecond=nonPeakRequestsPerSecond
  )
else:
  totalAppRunnerCharges = calcAppRunnerCharge(requestsPerSecond=requestsPerSecond)

# print("Total lambda compute charges : " + str(round(totalLambdaComputeCharges,3)) + " USD")
# print("Total lambda request charges : " + str(round(totalLambdaRequestCharges,3)) + " USD")
print("Total lambda charges : " + str(round(totalLambdaCharges, 3)) + " USD")
print("Total App Runner Charges : " + str(round(totalAppRunnerCharges, 3)) + " USD")

