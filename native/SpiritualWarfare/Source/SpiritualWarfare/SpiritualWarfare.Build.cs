using UnrealBuildTool;

public class SpiritualWarfare : ModuleRules
{
    public SpiritualWarfare(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
        PublicDependencyModuleNames.AddRange(new string[]
        {
            "Core", "CoreUObject", "Engine", "InputCore", "EnhancedInput",
            "GameplayTags", "GameplayTasks", "AIModule", "Niagara"
        });
    }
}
