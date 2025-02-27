"""
Module for generating Anki decks from translated words.
"""
import random
import logging
import genanki

def create_anki_deck(translations, output_file):
    """Erstellt ein Anki-Deck aus den übersetzten Wörtern."""
    logging.info(f"Erstelle Anki-Deck mit {len(translations)} Karten")
    
    try:
        # Erstelle eindeutige IDs
        deck_id = random.randint(1 << 30, 1 << 31)
        model_id = random.randint(1 << 30, 1 << 31)
        
        logging.debug(f"Deck ID: {deck_id}, Model ID: {model_id}")
        
        try:
            deck = genanki.Deck(deck_id, "Russische Vokabeln")
            
            # Anki Note Model
            model = genanki.Model(
                model_id,
                "Russisch -> Deutsch",
                fields=[
                    {"name": "Russisch"},
                    {"name": "Deutsch"},
                    {"name": "Wortart"},
                    {"name": "Grammatik"},
                    {"name": "Beispiel_DE"},
                    {"name": "Beispiel_RU"}
                ],
                templates=[{
                    "name": "Russisch -> Deutsch",
                    "qfmt": """
                        <div class="russian">{{Russisch}}</div>
                    """,
                    "afmt": """
                        <div class="russian">{{Russisch}}</div>
                        <hr>
                        <div class="translation">{{Deutsch}}</div>
                        <div class="part-of-speech"><i>{{Wortart}}</i></div>
                        <div class="grammar"><small>{{Grammatik}}</small></div>
                        <hr>
                        <div class="example">
                            <div class="example-ru">{{Beispiel_RU}}</div>
                            <div class="example-de">{{Beispiel_DE}}</div>
                        </div>
                        <style>
                            .card {
                                font-family: Arial, sans-serif;
                                font-size: 20px;
                                text-align: center;
                                color: black;
                                background-color: white;
                            }
                            .russian { 
                                font-size: 28px;
                                color: #2196F3;
                                margin-bottom: 10px;
                            }
                            .translation {
                                font-size: 24px;
                                color: #4CAF50;
                                margin-bottom: 8px;
                            }
                            .part-of-speech {
                                color: #9E9E9E;
                                margin-bottom: 5px;
                            }
                            .grammar {
                                color: #757575;
                                margin-bottom: 15px;
                            }
                            .example {
                                font-style: italic;
                                color: #666;
                                margin-top: 15px;
                            }
                            .example-ru {
                                margin-bottom: 5px;
                            }
                            hr {
                                border: none;
                                border-top: 1px solid #E0E0E0;
                                margin: 10px 0;
                            }
                        </style>
                    """,
                }]
            )
            
            # Füge Karten hinzu
            for i, trans in enumerate(translations, 1):
                try:
                    note = genanki.Note(
                        model=model,
                        fields=[
                            trans["original"],
                            trans["translation"],
                            trans["part_of_speech"],
                            trans.get("grammar_info", ""),  # Optional
                            trans.get("example_de", ""),    # Optional
                            trans.get("example_ru", "")     # Optional
                        ]
                    )
                    deck.add_note(note)
                    logging.debug(f"Karte {i} hinzugefügt: {trans['original']} -> {trans['translation']}")
                except Exception as e:
                    logging.error(f"Fehler beim Hinzufügen der Karte {i}: {str(e)}")
            
            # Speichere das Deck
            genanki.Package(deck).write_to_file(output_file)
            logging.info(f"Anki-Deck erfolgreich erstellt: {output_file}")
            
        except Exception as e:
            logging.error(f"Fehler beim Erstellen des Decks: {str(e)}", exc_info=True)
            raise
            
    except Exception as e:
        logging.error(f"Unerwarteter Fehler beim Erstellen des Anki-Decks: {str(e)}", exc_info=True)
        raise
