import os
import traceback

from modules.model.FluxModel import FluxModel
from modules.util.ModelNames import ModelNames

import torch

from safetensors.torch import load_file


class FluxLoRALoader:
    def __init__(self):
        super(FluxLoRALoader, self).__init__()

    def __load_safetensors(
            self,
            model: FluxModel,
            lora_name: str,
    ):
        model.lora_state_dict = load_file(lora_name)

    def __load_ckpt(
            self,
            model: FluxModel,
            lora_name: str,
    ):
        model.lora_state_dict = torch.load(lora_name)

    def __load_internal(
            self,
            model: FluxModel,
            lora_name: str,
    ):
        if os.path.exists(os.path.join(lora_name, "meta.json")):
            safetensors_lora_name = os.path.join(lora_name, "lora", "lora.safetensors")
            if os.path.exists(safetensors_lora_name):
                self.__load_safetensors(model, safetensors_lora_name)
        else:
            raise Exception("not an internal model")

    def load(
            self,
            model: FluxModel,
            model_names: ModelNames,
    ):
        stacktraces = []

        if model_names.lora == "":
            return

        try:
            self.__load_internal(model, model_names.lora)
            return
        except:
            stacktraces.append(traceback.format_exc())

        try:
            self.__load_ckpt(model, model_names.lora)
            return
        except:
            stacktraces.append(traceback.format_exc())

        try:
            self.__load_safetensors(model, model_names.lora)
            return
        except:
            stacktraces.append(traceback.format_exc())

        for stacktrace in stacktraces:
            print(stacktrace)
        raise Exception("could not load LoRA: " + model_names.lora)