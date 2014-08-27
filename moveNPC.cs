// moveNPC taken from http://opensimulator.org/wiki/OsNpcCreate

moveNpc(key npc, vector dest) {
    //calculate distance to dest
    vector distance = dest - osNpcGetPos(npc);
    float dist = llSqrt((llAbs(llRound(distance.x)) * llAbs(llRound(distance.x))) + (llAbs(llRound(distance.y)) * llAbs(llRound(distance.y))) + (llAbs(llRound(distance.z)) * llAbs(llRound(distance.z))));
    
    //calculate how long it will take npc to reach dest
    integer time = llCeil(dist / 2.5);
    
    osNpcMoveToTarget(npc, dest, OS_NPC_NO_FLY);
    llSleep(time);
}
