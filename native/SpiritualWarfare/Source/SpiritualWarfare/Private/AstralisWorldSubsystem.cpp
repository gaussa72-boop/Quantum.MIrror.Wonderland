#include "AstralisWorldSubsystem.h"

void UAstralisWorldSubsystem::GenerateRegionProfiles(int32 Seed, int32 RegionCount, int32 PlayerLevel)
{
    Regions.Reset();
    const int32 SafeCount = FMath::Clamp(RegionCount, 1, 256);
    const int32 SafeLevel = FMath::Clamp(PlayerLevel, 1, 999);
    FRandomStream Random(Seed);
    for (int32 Index = 0; Index < SafeCount; ++Index)
    {
        FAstralisRegionProfile Region;
        Region.RegionId = FName(*FString::Printf(TEXT("astralis-region-%03d"), Index + 1));
        Region.Biome = static_cast<EAstralisBiome>(Random.RandRange(0, 4));
        Region.ThreatLevel = Random.FRandRange(0.05f, 1.0f);
        Region.RecommendedLevel = FMath::Clamp(
            SafeLevel + Random.RandRange(-5, 12) + Index / 2, 1, 999);
        Regions.Add(MoveTemp(Region));
    }
}

void UAstralisWorldSubsystem::RegisterNPC(const FAstralisNPCProfile& Profile)
{
    if (Profile.CharacterId.IsNone())
    {
        return;
    }
    const int32 ExistingIndex = NPCProfiles.IndexOfByPredicate(
        [&Profile](const FAstralisNPCProfile& Item)
        {
            return Item.CharacterId == Profile.CharacterId;
        });
    if (ExistingIndex == INDEX_NONE)
    {
        NPCProfiles.Add(Profile);
    }
    else
    {
        NPCProfiles[ExistingIndex] = Profile;
    }
}
