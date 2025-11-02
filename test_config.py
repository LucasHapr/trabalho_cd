"""Script para testar a configuração do Hydra"""
from pathlib import Path
from hydra import compose, initialize_config_dir

print("Testando configuração Hydra...")
print(f"Diretório: {Path('conf').absolute()}")

try:
    config_dir = Path(__file__).parent / "conf"
    with initialize_config_dir(config_dir=str(config_dir.absolute()), version_base=None):
        cfg = compose(config_name="config")
        
        print("\n✓ Configuração carregada com sucesso!")
        print(f"\nKeys disponíveis: {list(cfg.keys())}")
        
        if hasattr(cfg, 'data'):
            print("\n✓ cfg.data existe!")
            print(f"  - external.path: {cfg.data.external.path}")
            print(f"  - wearable.path: {cfg.data.wearable.path}")
        else:
            print("\n✗ cfg.data NÃO existe!")
            
except Exception as e:
    print(f"\n✗ Erro: {e}")
    import traceback
    traceback.print_exc()
