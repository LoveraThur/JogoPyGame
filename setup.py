# pip install cx_freeze
import cx_Freeze
executaveis = [ 
               cx_Freeze.Executable(
                   script="main.py", 
                   icon="bases/icone.ico",
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

# python setup.py build
# python setup.py bdist_msi