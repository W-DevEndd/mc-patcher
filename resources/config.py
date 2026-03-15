
class Config:
    # Apks
    minecraft_apk = "./files/arm64-v8a/minecraft.apk"
    minecraft_apk_32 = "./files/armebi-v7a/minecraft.apk"

    # Material bin loader
    mbloader_patch = True
    mb_libso = "./files/arm64-v8a/libmtbinloader2.so"
    mb_libso_32 = "./files/armebi-v7a/libmtbinloader2.so"

    make_32 = False

    force_unlock_visual = True