#pragma once

#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "AstralisWorldSubsystem.generated.h"

UENUM(BlueprintType)
enum class EAstralisBiome : uint8
{
    CelestialHighlands,
    Elderwood,
    AstralDesert,
    VoidFrontier,
    CrystalSea
};

USTRUCT(BlueprintType)
struct FAstralisRegionProfile
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FName RegionId = NAME_None;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EAstralisBiome Biome = EAstralisBiome::CelestialHighlands;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float ThreatLevel = 0.25f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 RecommendedLevel = 1;
};

USTRUCT(BlueprintType)
struct FAstralisNPCProfile
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FName CharacterId = NAME_None;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FName Archetype = TEXT("Wanderer");

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FName Faction = TEXT("Unaligned");

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float Disposition = 0.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString MemorySummary;
};

UCLASS()
class SPIRITUALWARFARE_API UAstralisWorldSubsystem : public UWorldSubsystem
{
    GENERATED_BODY()

public:
    UFUNCTION(BlueprintCallable, Category="Astralis|World")
    void GenerateRegionProfiles(int32 Seed, int32 RegionCount, int32 PlayerLevel);

    UFUNCTION(BlueprintPure, Category="Astralis|World")
    const TArray<FAstralisRegionProfile>& GetRegions() const { return Regions; }

    UFUNCTION(BlueprintCallable, Category="Astralis|NPC")
    void RegisterNPC(const FAstralisNPCProfile& Profile);

    UFUNCTION(BlueprintPure, Category="Astralis|NPC")
    const TArray<FAstralisNPCProfile>& GetNPCProfiles() const { return NPCProfiles; }

private:
    UPROPERTY(VisibleAnywhere, Category="Astralis|World")
    TArray<FAstralisRegionProfile> Regions;

    UPROPERTY(VisibleAnywhere, Category="Astralis|NPC")
    TArray<FAstralisNPCProfile> NPCProfiles;
};
