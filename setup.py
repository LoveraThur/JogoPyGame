import cx_Freeze
executaveis = [ 
               cx_Freeze.Executable(
                   script="main.py", 
                   icon="bases/icon.ico",
                    target_name="MinecraftEnd.exe"
                   ) ]
cx_Freeze.setup(
    name = "End Minecraft",
    options={
        "build_exe":{
            "packages":["pygame", "pyttsx3"],
            "include_files":["bases","recursos"]
        }
    }, executables = executaveis
)
