<script setup>
/* eslint-disable */

// props
const props = defineProps({
    type: {type: String, default: "text"},
    label: {type: String, default: "Label"},
    required: {type: Boolean, default: true},
    minLen: {type: Number, default: 0},
    maxLen: {type: Number, default: 255},
    iconPos: {type: String, default: "right"},
    disable: {type: Boolean, default: false },
    autocomplete: {type: Boolean, default: false},
    modelValue: {type: String},
    modelModifiers: { default: () => ({}) }
})

// emits
const emit = defineEmits(["update:modelValue"])

// methods
const emitValue = (e) => {
    let value = e.target.value

    if (props.modelModifiers.capitalize) {
        value = value.charAt(0).toUpperCase() + value.slice(1)
    }
    else if (props.modelModifiers.lower) {
        value = value.toLowerCase()
    }

    emit("update:modelValue", value)
}
</script>

<template>
    <main
        :class="props.iconPos == 'left' ? 'gap-3':'', props.disable ? 'bg-gray-200':'hover:ring hover:ring-blue-400 focus-within:ring focus-within:ring-blue-400'"
        class="w-full p-2 flex items-center ring-1 ring-gray-200 ring-offset-white rounded overflow-hidden transition-all duration-300
        ">

        <input
            :type="props.type"
            :name="props.label"
            :id="props.label"
            :required="props.required"
            :minlength="props.minLen"
            :min="props.minLen"
            :maxlength="props.maxLen"
            :max="props.maxLen"
            :placeholder="props.label"
            :autocomplete="autocomplete"
            :disabled="props.disable"
            :value="modelValue"
            @input="emitValue"
            :class="props.iconPos == 'left' ? 'order-2':'', props.disable ? 'cursor-not-allowed':''"
            class="w-full bg-transparent text-xs text-gray-700 placeholder:text-gray-400 focus:outline-none md:text-sm"/>

        <slot name="icon">
            <!-- <IconPencilOutline class="w-5 h-5 stroke-gray-400" /> -->
        </slot>

    </main>
</template>