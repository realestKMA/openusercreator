<script setup>
/* eslint-disable */
import { ref } from 'vue';
import { RouterLink } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import AppInputField from './AppInputField.vue';
import IconUserCircleOutline from './icons/IconUserCircleOutline.vue';
import IconEnvelopeOutline from './icons/IconEnvelopeOutline.vue';
import AppPasswordField from './AppPasswordField.vue';
import AppButton from './AppButton.vue';
import IconExclamationTraingleOutline from './icons/IconExclamationTraingleOutline.vue';
import IconGithub from './icons/IconGithub.vue';
import IconGoogle from './icons/IconGoogle.vue';
import IconTwitter from './icons/IconTwitter.vue';
import IconKeyOutline from './icons/IconKeyOutline.vue';

// refs
const username = ref("")
const email = ref("")
const password1 = ref("")
const password2 = ref("")
const loading = ref(false)

// stores
const authStore = useAuthStore()
</script>
    
<template>
    <main class="w-full h-full bg-transparent">

        <!-- form inputs -->
        <div class="h-full flex flex-col items-center mt-28">

            <!-- header -->
            <div class="w-full flex flex-col">
                <div class="my-6 self-start px-6 py-2 flex items-center justify-center p-2 rounded bg-gray-900">
                    <IconGithub v-if="authStore.social == 'github'" class="w-7 h-7 fill-white" />
                    <IconTwitter v-else-if="authStore.social == 'twitter'" class="w-7 h-7 fill-white" />
                    <IconGoogle v-else-if="authStore.social == 'google'" class="w-7 h-7 fill-white" />
                </div>
                <h3 class="text-3xl text-gray-900 font-semibold capitalize sm:text-4xl">Connect via
                    {{authStore.social}}</h3>
                <span class="mt-2 flex items-center gap-2">
                    <p class="text-xs text-gray-400 font-normal sm:text-sm">Already a creator?</p>
                    <RouterLink :to="{name: 'signin'}"
                        class="text-xs text-blue-400 font-medium hover:text-blue-500 sm:text-sm">Signin</RouterLink>
                </span>
            </div>

            <!-- form errors -->
            <div class="hidden mt-7 w-full list-inside list-disc">
                <span class="flex items-center gap-2">
                    <IconExclamationTraingleOutline class="w-4 h-4 stroke-red-500" />
                    <p class="text-xs text-red-500 font-normal md:text-sm">Hello world</p>
                </span>
            </div>
            <!-- form errors -->

            <form @submit.prevent="loading = !loading" class="w-full flex flex-col gap-4 mt-12 mb-5">
                <AppInputField v-model="username" type="text" label="Username" :minLen="4" :maxLen="15"
                    iconPos="left" :disable="loading" class="bg-gray-50">
                    <template #icon>
                        <IconUserCircleOutline class="w-5 h-5 stroke-gray-400" />
                    </template>
                </AppInputField>
                <AppInputField v-model="email" type="email" label="email" iconPos="left" :disable="loading" class="bg-gray-50">
                    <template #icon>
                        <IconEnvelopeOutline class="w-5 h-5 stroke-gray-400" />
                    </template>
                </AppInputField>
                <div class="grid grid-cols-1 gap-4 pb-2 sm:grid-cols-2">
                    <AppPasswordField v-model="password1" label="Password" :disable="loading" class="bg-gray-50">
                        <template #icon>
                            <IconKeyOutline class="w-5 h-5 stroke-gray-400" />
                        </template>
                    </AppPasswordField>
                    <AppPasswordField v-model="password2" label="Confirm password" :disable="loading" class="bg-gray-50">
                        <template #icon>
                            <IconKeyOutline class="w-5 h-5 stroke-gray-400" />
                        </template>
                    </AppPasswordField>
                </div>
                <AppButton label="Create Account" type="submit" :loading="loading"
                    class="text-white bg-blue-500 hover:bg-blue-600 disabled:bg-blue-300" />
            </form>

        </div>
        <!-- form inputs -->

    </main>
</template>