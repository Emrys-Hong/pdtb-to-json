def data_generator_per_doc_sentence_level(section, filenumber, relation_id, batch_idx, rawtext):
    """generate json format data for one document
    Args:
            section(str): 0~24
            filenumber(str): 0~99
            relation_id(int): relation_id is unique accross every relation, this is start relation_id
            batch_idx(list[int]): list of corresponding int from same file
            rawtext(str): rawtext of that doc
    Returns:
            pdtb-json
            pdtb-data
    """
    # for data
    doc_data, doc_lookup = get_data_prototype(section, filenumber, relation_id, batch_idx)
    doc = tokenizor(rawtext)
    words = get_word_index(doc)
    linkers = get_linker(words, doc_lookup)
    
    # for parse
    sentences = []
    
    sentence_token_offset = 0
    # for each token in document
    for sentence_id, sentence in enumerate(doc.sents):
        if sentence_id == 0:
            continue
        else:
            sent = str(sentence)
                
            # begin of the new round
            words = []
            dependencies = dependency_parse(sent)
            parsetree = constituent_parsing(sent)
            
            sent_char_index = rawtext.index(sent)

            
            for tok in tokenizor(sent):
                ## 5 attribute of each word
                char_offset_begin = sent_char_index + tok.idx
                char_offset_end = sent_char_index + tok.idx + len(tok)
                token_offset_in_doc = sentence_token_offset + tok.i
                sentence_offset = sentence_id
                token_offset_in_sent = tok.i
                
                linker = linkers[token_offset_in_doc]
                token_dict = {'CharacterOffsetBegin': char_offset_begin, "CharacterOffsetEnd": char_offset_end, 
                              "PartOfSpeech": tok.pos_, "Linkers": linker}
                words.append([tok.text, token_dict])

                token_list = [char_offset_begin, char_offset_end, token_offset_in_doc, 
                              sentence_offset, token_offset_in_sent]
                add_token_list(doc_data, linker, token_list)
            
            sentence_token_offset += len(sentence)
            sentences.append({"dependencies": dependencies, "parsetree": parsetree, "words": words})
            
    return {'sentences': sentences} , doc_data

def data_generator_per_doc_token_level_old(section, filenumber, relation_id, batch_idx, rawtext):
    """generate json format data for one document
    Args:
            section(str): 0~24
            filenumber(str): 0~99
            relation_id(int): relation_id is unique accross every relation, this is start relation_id
            batch_idx(list[int]): list of corresponding int from same file
            rawtext(str): rawtext of that doc
    Returns:
            pdtb-json
            pdtb-data
    """
    # for data
    doc_data, doc_lookup = get_data_prototype(section, filenumber, relation_id, batch_idx)
    doc = tokenizor(rawtext)
    words = get_word_index(doc)
    linkers = get_linker(words, doc_lookup)
    
    # for parse
    temp = None
    first_sent = None
    sentences = []
    # for each token in document
    for tok in doc:
        ## TODO: here need to change
        if temp == None:
            first_sent = str(tok.sent)
            temp = True
            continue
        elif str(tok.sent) == first_sent:
            continue
        else:
            if str(tok.sent) != temp:
                if type(first_sent) != str:# end of the previous round
                    sentences.append({"dependencies": dependencies, "parsetree": parsetree, 
                                      "words": words})
                
                # begin of the new round
                words = []
                temp = str(tok.sent)
                first_sent = False
                dependencies = dependency_parse(temp)
                parsetree = constituent_parsing(temp)
            
            ## 5 attribute of each word
            char_offset_begin = tok.idx
            char_offset_end = tok.idx + len(tok)
            token_offset_in_doc = tok.i
            sentence_offset = list(doc.sents).index(tok.sent)
            token_offset_in_sent = list(tok.sent).index(tok)
            
            linker = linkers[token_offset_in_doc]
            token_dict = {'CharacterOffsetBegin': char_offset_begin, "CharacterOffsetEnd": char_offset_end, 
                          "PartOfSpeech": tok.pos_, "Linkers": linker}
            words.append([tok.text, token_dict])
            
            token_list = [char_offset_begin, char_offset_end, token_offset_in_doc, 
                          sentence_offset, token_offset_in_sent]
            add_token_list(doc_data, linker, token_list)
            
    return {'sentences': sentences} , doc_data

def constituent_parse_old(sent):
    return nlp.parse(sent).replace('ROOT', " ").replace('   ', ' ').replace('  ', ' ')
