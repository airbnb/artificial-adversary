from Adversary import Adversary

def test_generate_single_iter():
    m = Adversary(verbose=True)
    og_texts = [u'happy happy happy happy dog dog dog dog dog',
          u'okay okay yeah here', 'tell me awful things']
    g = m.generate(og_texts)
    assert(len(g) == 3)

def test_generate_many_iter():
    m = Adversary(verbose=True)
    og_texts = [u'happy happy happy happy dog dog dog dog dog',
          u'okay okay yeah here', 'tell me awful things']
    g = m.generate(og_texts, text_sample_rate=5)
    assert(len(g) == 15)

def test_large():
    m = Adversary(verbose=True)
    og_texts = ['tell me awful things'] * 1000
    g = m.generate(og_texts, text_sample_rate=5)
    assert (len(g) == 5000)

def test_attack():
    m = Adversary(verbose=True)
    og_texts = [u'happy happy happy happy dog dog dog dog dog',
          u'okay okay yeah here', 'tell me awful things']
    g = m.generate(og_texts)
    df_s, df_m = m.attack(og_texts, g, lambda x: 1 if x in og_texts else 0)
    assert(df_s is not None and df_m is not None)

def test_attack_large():
    m = Adversary(verbose=True)
    og_texts = ['tell me awful things'] * 1000
    g = m.generate(og_texts)
    df_s, df_m = m.attack(og_texts, g, lambda x: 1 if x in og_texts else 0)
    assert (df_s is not None and df_m is not None)
