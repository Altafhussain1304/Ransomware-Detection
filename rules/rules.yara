rule SuspiciousEncryptionBehavior
{
    meta:
        description = "Detects possible ransomware encryption behavior (e.g., repetitive extensions)"
    strings:
        $ext1 = ".locked"
        $ext2 = ".encrypted"
        $ext3 = ".crypto"
    condition:
        any of ($ext*)
}

rule SuspiciousFileNames
{
    meta:
        description = "Detects ransom notes by common keywords"
    strings:
        $note1 = "YOUR FILES ARE ENCRYPTED"
        $note2 = "DECRYPTION INSTRUCTIONS"
        $note3 = "ransomware"
    condition:
        any of ($note*)
}
