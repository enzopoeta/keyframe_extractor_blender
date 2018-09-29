import random
import operator
import bpy
import collections


initialFrame = 0 #bpy.context.scene.frame_start
finalFrame = 230 #bpy.context.scene.frame_end
#initialFrame = 1
#finalFrame = 250
individualNumberOfFrames = 138

def generatePopulation(popSize,individualData,fitnessData) :
            
        for i in range(0, popSize-1) :
                individualData.append(generateIndividual(individualNumberOfFrames))
                fitnessData.append(obtainFitness(individualData[i]))
                

#participants=[]
#scoreData=[0]*len(participants)
def doTorney(numberOfChallenges,participantsFitness,scoreData) :
        populationSize=len(participantsFitness)
        
        for x in range(0,populationSize-1) :
                opponentIndexes=[]
                for y in range(0,numberOfChallenges-1) :
                        opponentIndexes.append(random.randrange(0, populationSize-1,1 ))
                me=participantsFitness[x]
                for z in opponentIndexes :
                        opponent=participantsFitness[z]
                        if me>=opponent :
                                scoreData[x]+=1
                        else :
                                scoreData[z]+=1
def rebuildMovementFromKeyFrames(individual) :
        scene = bpy.context.scene
        bpyContext=bpy.context
        obj=bpyContext.object
        armature=obj.data
        interpolatedIntervalData ={}
        #print (individual)
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.select_all(action='TOGGLE')
        
        for x in range(0,len(individual)-2) :
                initialFrame = individual[x]
                finalFrame = individual[x+1]
                interpolatedIntervalData = generateFrameInterval(initialFrame,finalFrame)

                for i in range(initialFrame, finalFrame) :
                        scene.frame_set(i)
                        #print(i)
                        #print(interpolatedIntervalData.keys())
                        generatedFrame=interpolatedIntervalData[i]
                        for bone in armature.bones :
                                poseBone = obj.pose.bones[bone.name]
                                generatedBone = generatedFrame[bone.name]
                                
                                #print('frame : ',i)
                                #print('bone_name: ',bone.name)
                                #print('before')
                                #print(poseBone.rotation_euler)
                                
                                poseBone.rotation_euler[0]=generatedBone[0]
                                poseBone.rotation_euler[1]=generatedBone[1]
                                poseBone.rotation_euler[2]=generatedBone[2]
                                poseBone.location[0]=generatedBone[3]
                                poseBone.location[1]=generatedBone[4]
                                poseBone.location[2]=generatedBone[5]
                                
                                #print('trying to set this')
                                #print(generatedBone)
                                #print('After')
                                #print(poseBone.rotation_euler)
                                
                                bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
                                scene.update()        
        bpy.ops.object.mode_set(mode='OBJECT')

def doSelection(numberOfSurvivors,populationTourneyScore,populationFitnessData,populationData) :
        while len(populationData) > numberOfSurvivors :
                minorScore=min(populationTourneyScore)
                minorScoreIndex=populationTourneyScore.index(minorScore)
                del populationTourneyScore[minorScoreIndex]
                del populationFitnessData[minorScoreIndex]
                del populationData[minorScoreIndex]


def generateFrameInterval(iniFrame,finFrame) :
        

        scene = bpy.context.scene
        frameStart =iniFrame
        frameEnd=finFrame
        interpolatedIntervalData ={}
        

        bpyContext=bpy.context
        obj=bpyContext.object
        armature=obj.data

        scene.frame_set(frameStart)
        initialFrameData={} 
        for bone in armature.bones:
                # print(bone.name)
                xyz=[]
                poseBone = obj.pose.bones[bone.name]
                xyz.append(poseBone.rotation_euler[0])
                xyz.append(poseBone.rotation_euler[1])
                xyz.append(poseBone.rotation_euler[2])
                xyz.append(poseBone.location[0])
                xyz.append(poseBone.location[1])
                xyz.append(poseBone.location[2])
                initialFrameData[bone.name]=xyz
        interpolatedIntervalData[frameStart]=initialFrameData
        # print(interpolatedIntervalData[1].keys())
        
        scene.frame_set(frameEnd)
        finalFrameData={} 
        for bone in armature.bones:
                xyz=[]
                poseBone = obj.pose.bones[bone.name]
                xyz.append(poseBone.rotation_euler[0])
                xyz.append(poseBone.rotation_euler[1])
                xyz.append(poseBone.rotation_euler[2])
                xyz.append(poseBone.location[0])
                xyz.append(poseBone.location[1])
                xyz.append(poseBone.location[2])
                finalFrameData[bone.name]=xyz
        interpolatedIntervalData[frameEnd]=finalFrameData
        # print(interpolatedIntervalData[50].keys())
        
        interpolationDataIncrement={}
        numberOfFrames=abs(frameEnd - frameStart)   
        
        if numberOfFrames >= 1 :
            
                for bone in armature.bones:
                        currentBone=bone.name
                        stepXYZ=[]
                        initXYZ=initialFrameData[currentBone]
                        fimXYZ=finalFrameData[currentBone]
                        if fimXYZ[0] < initXYZ[0] :
                                stepXYZ.append(-(abs(fimXYZ[0]-initXYZ[0])/numberOfFrames))
                        else :
                                stepXYZ.append(abs(fimXYZ[0]-initXYZ[0])/numberOfFrames)
                        if fimXYZ[1] < initXYZ[1] :
                                stepXYZ.append(-(abs(fimXYZ[1]-initXYZ[1])/numberOfFrames))
                        else :
                                stepXYZ.append(abs(fimXYZ[1]-initXYZ[1])/numberOfFrames)
                        if fimXYZ[2] < initXYZ[2] :
                                stepXYZ.append(-(abs(fimXYZ[2]-initXYZ[2])/numberOfFrames))
                        else :
                                stepXYZ.append(abs(fimXYZ[2]-initXYZ[2])/numberOfFrames)
                        
                        if fimXYZ[3] < initXYZ[3] :
                                stepXYZ.append(-(abs(fimXYZ[3]-initXYZ[3])/numberOfFrames))
                        else :
                                stepXYZ.append(abs(fimXYZ[3]-initXYZ[3])/numberOfFrames)
                                
                        if fimXYZ[4] < initXYZ[4] :
                                stepXYZ.append(-(abs(fimXYZ[4]-initXYZ[4])/numberOfFrames))
                        else :
                                stepXYZ.append(abs(fimXYZ[4]-initXYZ[4])/numberOfFrames)
                                
                        if fimXYZ[5] < initXYZ[5] :
                                stepXYZ.append(-(abs(fimXYZ[5]-initXYZ[5])/numberOfFrames))
                        else :
                                stepXYZ.append(abs(fimXYZ[5]-initXYZ[5])/numberOfFrames)
                                

                        interpolationDataIncrement[currentBone]=stepXYZ
                # print(interpolationDataIncrement.keys())
                generatedFrameIndexes=range(frameStart+1, frameEnd)
                # print(generatedFrameIndexes)
                for frameIndex in generatedFrameIndexes :
                        interpolatedFrameData={}
                        for bone in armature.bones:
                                currentBone=bone.name
                                initXYZ=initialFrameData[currentBone]
                                stepIncrementXYZ=interpolationDataIncrement[currentBone]
                                frameInternalIndex=generatedFrameIndexes.index(frameIndex)
                                xyz=[]
                                poseBone = obj.pose.bones[bone.name]
                                xyz.append(initXYZ[0]+(stepIncrementXYZ[0]*(frameInternalIndex+1)))
                                xyz.append(initXYZ[1]+(stepIncrementXYZ[1]*(frameInternalIndex+1)))
                                xyz.append(initXYZ[2]+(stepIncrementXYZ[2]*(frameInternalIndex+1)))
                                xyz.append(initXYZ[3]+(stepIncrementXYZ[3]*(frameInternalIndex+1)))
                                xyz.append(initXYZ[4]+(stepIncrementXYZ[4]*(frameInternalIndex+1)))
                                xyz.append(initXYZ[5]+(stepIncrementXYZ[5]*(frameInternalIndex+1)))

                                interpolatedFrameData[currentBone]=xyz
                        #if frameIndex==2 :
                                #print(interpolatedFrameData.keys())
                                
                        interpolatedIntervalData[frameIndex]=interpolatedFrameData
               
        return interpolatedIntervalData


def obtainFitness( anIndividual) :
        
        scene = bpy.context.scene
        
        bpyContext=bpy.context
        obj=bpyContext.object
        armature=obj.data
    
        individualSize = len(anIndividual)
        differenceAcumulator = 0
        #d.values()[i]
        for x in range(0, individualSize-1) :
                firstFrameInterval=anIndividual[x]
                lastFrameInterval=anIndividual[x+1]
                interpolatedIntervalData = generateFrameInterval(firstFrameInterval,lastFrameInterval)
                for i in range(firstFrameInterval, lastFrameInterval) :
                        scene.frame_set(i)
                        #print(i)
                        #print(interpolatedIntervalData.keys())
                        generatedFrame=interpolatedIntervalData[i]
                        for bone in armature.bones :
                                poseBone = obj.pose.bones[bone.name]
                                generatedBone = generatedFrame[bone.name]
                                diffX=abs(poseBone.rotation_euler[0]-generatedBone[0])
                                differenceAcumulator+=diffX
                                diffY=abs(poseBone.rotation_euler[1]-generatedBone[1])
                                differenceAcumulator+=diffY
                                diffZ=abs(poseBone.rotation_euler[2]-generatedBone[2])
                                differenceAcumulator+=diffZ
        fitness =1/(1+differenceAcumulator)
        
        return fitness


def mutateIndividual(individual,geneMutationChance) :
        individualCopy=individual[:]
        for x in individualCopy :
                #print(x)
                if x != initialFrame and x != finalFrame :
                        diceResult=random.randrange(0, 100, 1)
                        if diceResult <= geneMutationChance :
                                newFrame = random.randrange(initialFrame, finalFrame, 1)
                                while newFrame in individualCopy :
                                        newFrame = random.randrange(initialFrame, finalFrame, 1)
                                individualCopy[individualCopy.index(x)]=newFrame

        

        individualCopy.sort()
        return individualCopy;



def generateIndividual(numberOfFrames) :

        # numero de frames do individuo
        individualNumberOfFrames = numberOfFrames
        if individualNumberOfFrames <= 0 :
                individualNumberOfFrames = 1
        individual = []
        
        # adicionando o primeiro e o ultimo frame
        if not(initialFrame in individual) :
                individual.append(initialFrame)
        if not(finalFrame in individual) :
                individual.append(finalFrame)


        for x in range(0, individualNumberOfFrames-1) :
                if len(individual) < numberOfFrames :
                        frameIndex = random.randrange(initialFrame, finalFrame, 1)
                        while frameIndex in individual :
                                frameIndex = random.randrange(initialFrame, finalFrame, 1)
                        individual.append(frameIndex)



        individual.sort()
        return individual;

def crossOver(individual1,individual2) :
        individual1Size = len(individual1)
        individual2Size= len(individual2)
        
        individual1CutPoint = individual1Size // 2 
        individual2CutPoint = individual2Size // 2 
        
            
        sons = []
        son1 = individual1[1:individual1CutPoint] + individual2[individual2CutPoint:individual2Size-1]
        son2 = individual2[1:individual2CutPoint] + individual1[individual1CutPoint:individual1Size-1]
        
        # adicionando o primeiro e o ultimo frame
        if not(initialFrame in son1) :
                son1.append(initialFrame)
        if not(finalFrame in son1) :
                son1.append(finalFrame)
        
        if not(initialFrame in son2) :
                son2.append(initialFrame)
        if not(finalFrame in son2) :
                son2.append(finalFrame)

        #tentando eliminar repeticoes de frames
        son1Set=set(son1)
        son1Temp=list(son1)
        for x in range(0,individual1Size-1) :
                if len(son1Temp) < individual1Size :
                        if individual1[x] not in son1TempList :
                                son1Temp.append(individual1[x])
        if len(son1Temp) == individual1Size :
                son1=son1Temp
                    
        son2Set=set(son2)
        son2Temp=list(son2)
        for x in range(0,individual1Size-1) :
                if len(son2Temp) < individual2Size :
                        if individual2[x] not in son2TempList :
                                son2Temp.append(individual2[x])
        if len(son2Temp) == individual2Size :
                son2=son2Temp
                        
        
        
        
        son1.sort()
        son2.sort()
        
        sons.append(son1)
        sons.append(son2)
        
        return sons;






def ga(numberOfIterations,populationData,populationFitnessData,fitnessOverTime) :
        
        #inicializando a populacao e o fitness dos individuos
        popSize=20
        
        generatePopulation(popSize,populationData,populationFitnessData)
        
        for x in range(1, numberOfIterations) :
                
                # adicionando um elemento aleatorio mutado
                randomIndividualIndex=random.randrange(0, len(populationData)-1, 1) 
                mutadedIndividual=mutateIndividual(populationData[randomIndividualIndex],30)
                mutadedIndividualFitness=obtainFitness(mutadedIndividual)
                populationData.append(mutadedIndividual)
                populationFitnessData.append(mutadedIndividualFitness)
                #if x==1 :
                        #print(populationFitnessData)
                
                
                # adicionando individuos criados via crossover
                numberOfCrossOvers=2
                
                
                for y in range(0, numberOfCrossOvers-1) :
                        firstIndividualIndex=random.randrange(0, len(populationData)-1, 1) 
                        secondIndividualIndex=random.randrange(0, len(populationData)-1, 1) 
                        while firstIndividualIndex == secondIndividualIndex :
                                secondIndividualIndex=random.randrange(0, len(populationData)-1, 1) 
                        sons = crossOver(populationData[firstIndividualIndex],populationData[secondIndividualIndex] )
                        populationData.append(sons[0])
                        populationFitnessData.append(obtainFitness(sons[0]))
                        
                        populationData.append(sons[1])
                        populationFitnessData.append(obtainFitness(sons[1]))
                 
                # efetuando competicao via torneio
                nOfChallenges=5
                scoreData=[0]*len(populationData)
                doTorney(nOfChallenges,populationFitnessData,scoreData)
                 
                #selecionando os individuos mais aptos
                doSelection(popSize,scoreData,populationFitnessData,populationData)
                 
                fitnessOverTime.append(populationFitnessData[:])                 


popData=[]
popFitnessData=[]
fitOverTime=[]
ga(150,popData,popFitnessData,fitOverTime)

#print(fitOverTime)

bestFitnessIndex = popFitnessData.index(max(popFitnessData))
rebuildMovementFromKeyFrames(popData[bestFitnessIndex])


#ind1 = generateIndividual(individualNumberOfFrames);
#ind2 = generateIndividual(individualNumberOfFrames);
#ind3 = mutateIndividual(ind2, 100)

#sons = crossOver(ind1, ind2)

#print(ind1)
#print(ind2)
#print(ind3)
#print(sons)

#interpolated_interval=generateFrameInterval(1,50)

#print(interpolated_interval.keys())

#print(interpolated_interval[3].values())

#fitness_test=obtainFitness(ind1)
#print (fitness_test)

#fitness_test2=obtainFitness(ind2)
#print (fitness_test2)


#popData=[]
#popFitness=[]

#generatePopulation(20,popData,popFitness)
#print(popFitness)