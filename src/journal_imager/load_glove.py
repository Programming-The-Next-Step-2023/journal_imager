import requests
import zipfile
import io
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models import KeyedVectors
from pathlib import Path

# Provide the path to the downloaded and extracted GloVe embeddings
# %cd src/journal_imager/glove.6B/
# glove_path = Path.cwd()
# glove_path = base_path / "glove.6B"

def load_glove():
    """ Load GloVe embeddings.
    
    Parameters:
        None

    Returns:
        gensim.models.keyedvectors.Word2VecKeyedVectors: embedding structure that contains keys (i.e., words) and their corresponding GloVe embeddings.
    """

    # Get path to GloVe embeddings
    glove_path = Path(__file__).parent / "assets/glove.6B"

    # Check if GloVe embeddings are already downloaded
    if not glove_path.exists():
        print('GloVe embeddings not found. Downloading...')
        
        # Provide the url to the GloVe embeddings
        url = 'http://nlp.stanford.edu/data/glove.6B.zip'

        # Download and extract the embeddings
        response = requests.get(url)

        # Create GloVe directory and extract the embeddings
        glove_path.mkdir()
        z = zipfile.ZipFile(io.BytesIO(response.content))
        z.extractall(glove_path)

        # Delete all files in the GloVe directory except 50d
        for file in glove_path.iterdir():
            if file.name != 'glove.6B.50d.txt':
                file.unlink()

    else:
        print('GloVe embeddings found.')

    # Check if GloVe embeddings are already converted to Word2Vec format
    word2vec_output_file = glove_path / (glove_path.name + '.word2vec')
    if not word2vec_output_file.exists():
        # Convert GloVe .txt file to Word2Vec file format
        print('Converting GloVe embeddings to Word2Vec format...')      
        glove2word2vec(glove_path / "glove.6B.50d.txt", word2vec_output_file)
    else:
        print('GloVe embeddings already in Word2Vec format.')

    return KeyedVectors.load_word2vec_format(word2vec_output_file, binary=False)