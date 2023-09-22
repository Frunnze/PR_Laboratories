from player import Player
import xmltodict
from dicttoxml import dicttoxml
import player_pb2


class PlayerFactory:
    def to_json(self, players):
        '''
            This function should transform a list of Player objects into a list with dictionaries.
        '''
        result = []

        for player in players:
            d = {}
            d["nickname"] = player.nickname
            d["email"] = player.email
            d["date_of_birth"] = player.date_of_birth.strftime('%Y-%m-%d')
            d["xp"] = player.xp
            d["class"] = player.cls
            result.append(d)

        return result
            

    def from_json(self, list_of_dict):
        '''
            This function should transform a list of dictionaries into a list with Player objects.
        '''
        player_objects = []

        for d in list_of_dict:
            player = Player(d['nickname'], d['email'], d['date_of_birth'], d['xp'], d['class'])
            player_objects.append(player)

        return player_objects


    def from_xml(self, xml_string):
        '''
            This function should transform a XML string into a list with Player objects.
        '''
        player_objects = []

        my_dict = xmltodict.parse(xml_string)
        if isinstance(my_dict['data']['player'], list):
            for d in list(my_dict['data']['player']):
                player = Player(d['nickname'], d['email'], d['date_of_birth'], int(d['xp']), d['class'])
                player_objects.append(player)
        else:
            d = my_dict['data']['player']
            player = Player(d['nickname'], d['email'], d['date_of_birth'], int(d['xp']), d['class'])
            player_objects.append(player)

        return player_objects

    def to_xml(self, list_of_players):
        '''
            This function should transform a list with Player objects into a XML string.
        '''

        players_dicts = []

        for player in list_of_players:
            player.date_of_birth = player.date_of_birth.strftime('%Y-%m-%d')
            player_atrr = vars(player)
            player_atrr['class'] = player_atrr['cls']
            del player_atrr['cls']
            players_dicts.append(player_atrr)

        xml = dicttoxml(players_dicts, attr_type=False, custom_root='data', item_func=lambda x: 'player')
        
        return xml

    def from_protobuf(self, binary):
        '''
            This function should transform a binary protobuf string into a list with Player objects.
        '''
        players = player_pb2.PlayersList()
        players.ParseFromString(binary)

        class_names = {0: "Berserk", 1: "Tank", 3: "Paladin", 4: "Mage"}
        player_objects = []
        for p in players.player:
            player = Player(p.nickname, p.email, p.date_of_birth, p.xp, class_names[p.cls])
            player_objects.append(player)
        
        return player_objects


    def to_protobuf(self, list_of_players):
        '''
            This function should transform a list with Player objects into a binary protobuf string.
        '''
        player_list = player_pb2.PlayersList()
        
        for player in list_of_players:
            p = player_list.player.add()
            p.nickname = player.nickname
            p.email = player.email
            p.date_of_birth = player.date_of_birth.strftime('%Y-%m-%d')
            p.xp = player.xp
            p.cls = player.cls

        return player_list.SerializeToString()