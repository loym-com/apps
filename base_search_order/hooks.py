def pre_init_hook(cr):
    cr.execute('ALTER TABLE ir_model ADD COLUMN IF NOT EXISTS order_custom VARCHAR;')
