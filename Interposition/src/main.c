//
//  main.c
//  LibraryFaultInjection
//
//  Created by Laurynas Karazija on 21/01/2016.
//  Copyright © 2016 Laurynas Karazija. All rights reserved.
//

#include "main.h"
#include "Orig.hpp"

#ifdef __APPLE__
__attribute__((section("__DATA,__mod_init_func"), used, aligned(sizeof(void*))))
#else
__attribute__((section(".init_array")))
#endif


typeof(fit_init) *__fit_init = fit_init;
#ifdef __APPLE__
__attribute__((section("__DATA,__mod_fini_func"), used, aligned(sizeof(void*))))
#else
__attribute__((section(".fini_array")))
#endif
typeof(fit_fini) *__fit_fin = fit_fini;

void fit_init()
{
    __FIT__injectionInit();
    //printf("My init\n");
}
void fit_fini()
{
    //printf("My fin\n");
    __FIT__injectionFin();
}