#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 11:53:48 2021

@author: mh
"""

import os
import pandas as pd


def get_tags(dictionary):
    """Get tags."""
    tags = [dictionary[key]["content"]["title"] for key in dictionary
            if dictionary[key]["content_type"] == "Tag"]
    return tags


def get_uuids_from_tag(dictionary, tag):
    """Get uuids from tag."""
    return dictionary[tag]


def get_notes_from_uuids(dictionary, uuid_list):
    """Get notes from UUIDs."""
    titles = []
    texts = []
    notes = []
    for key in dictionary:
        if dictionary[key]["content_type"] == "Note" and dictionary[key]["uuid"] in uuid_list:
            try:
                titles.append(dictionary[key]["content"]["title"])
                texts.append(dictionary[key]["content"]["text"])
                notes = list(zip(titles, texts))
            except KeyError:
                continue
    return notes


def write_notes_to_files(notes, tag):
    """Write notes to files."""
    # create directory
    path = tag
    if not os.path.exists(path):
        os.makedirs(path)
    # create files
    for note in notes:
        title = note[0].replace(" / ", " ")
        with open(path+"/"+title+".md", "w+") as file:
            file.write("# "+note[0])
            file.write("\n\n")
            file.write(note[1])
            file.write("\n\n")


def pipe():
    """Pipe all functions."""
    dataframe = pd.read_json("decrypted-sn-data.txt")
    df_dict = dataframe["items"].to_dict()

    print(get_tags(df_dict))

    # create tag–uuid dict
    uuids = {}
    for key in df_dict:
        if df_dict[key]["content_type"] == "Tag":
            title = df_dict[key]["content"]["title"]
            uuid_list = []
            for entry in df_dict[key]["content"]["references"]:
                try:
                    uuid_list.append(entry["uuid"])
                    uuids[title] = uuid_list
                except KeyError:
                    continue

    tag = input("Enter tag name: ")

    uuid_list = get_uuids_from_tag(uuids, tag)

    notes = get_notes_from_uuids(df_dict, uuid_list)

    write_notes_to_files(notes, tag)


if __name__ == "__main__":
    pipe()
